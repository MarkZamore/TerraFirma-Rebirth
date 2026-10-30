#!/usr/bin/env python3
"""Validate the reviewed native Options namespace and its exact source inputs.

Static scanning is a discovery tool. Publication uses this native snapshot and
fails if the source JAR set, descriptor, options, TSV or contexts drift from it.
This validates prepared evidence; it does not run Minecraft or recreate a capture.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent


class InvalidRegistry(ValueError):
    pass


def require(value, message):
    if not value:
        raise InvalidRegistry(message)


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, 'Duplicate JSON property: ' + key)
            result[key] = value
        return result
    return json.loads(path.read_text(encoding='utf-8-sig'), object_pairs_hook=unique)


def members(value, expected, where):
    require(type(value) is dict and set(value) == set(expected), 'Unexpected fields: ' + where)


def relative(value):
    require(type(value) is str and value and ':' not in value and '\\' not in value
            and not value.startswith('/') and all(part not in {'', '.', '..'} for part in value.split('/')),
            'Unsafe source path')
    return value


def ordinary(root, name):
    path = root.joinpath(*relative(name).split('/'))
    for item in [path, *path.parents]:
        require(not item.is_symlink() and not (item.exists() and getattr(item.lstat(), 'st_file_attributes', 0) & 0x400),
                'Linked source input: ' + name)
        if item == root:
            break
    return path


def names(value, where, allow_empty=False):
    require(type(value) is list and (value or allow_empty), 'Empty/invalid names: ' + where)
    require(all(type(name) is str and name and name == name.strip()
                and not any(c in name for c in ':\r\n\t') for name in value), 'Invalid name: ' + where)
    require(value == sorted(set(value)), 'Unsorted/duplicate names: ' + where)
    return set(value)


def records(value, where):
    require(type(value) is list and value, 'Empty/invalid source records: ' + where)
    result = {}
    for row in value:
        members(row, {'path', 'sizeBytes', 'sha256'}, where)
        name = relative(row['path'])
        require(name.casefold() not in {key.casefold() for key in result}, 'Duplicate source path')
        require(type(row['sizeBytes']) is int and row['sizeBytes'] >= 0
                and type(row['sha256']) is str and re.fullmatch('[a-f0-9]{64}', row['sha256']),
                'Invalid source integrity record')
        result[name] = row
    require(list(result) == sorted(result), 'Unsorted source records: ' + where)
    return result


def validate(pack: Path, tools: Path = HERE):
    pack = pack.resolve()
    snapshot_path = tools / 'native-registry.json'
    provenance = read(tools / 'preset-provenance.json')
    pin = provenance.get('nativeRegistry')
    members(pin, {'path', 'sha256'}, 'nativeRegistry provenance pin')
    require(pin['path'] == 'tools/keybinds/native-registry.json' and sha(snapshot_path) == pin['sha256'],
            'Native snapshot SHA256 pin mismatch')
    data = read(snapshot_path)
    members(data, {'schemaVersion', 'capture', 'optionsNames', 'allOnlyNames', 'sourceFiles', 'sourceMods'}, 'native snapshot')
    require(type(data['schemaVersion']) is int and data['schemaVersion'] == 1, 'Unsupported native snapshot schema')
    capture = data['capture']
    members(capture, {'sha256', 'sizeBytes', 'registeredAll', 'options'}, 'capture')
    require(type(capture['sha256']) is str and re.fullmatch('[a-f0-9]{64}', capture['sha256'])
            and type(capture['sizeBytes']) is int and capture['sizeBytes'] > 0,
            'Invalid native capture integrity fields')
    option_names = names(data['optionsNames'], 'Options')
    internal_names = names(data['allOnlyNames'], 'ALL-only', allow_empty=True)
    require(not option_names & internal_names, 'Options/ALL-only overlap')
    require(type(capture['options']) is int and capture['options'] == len(option_names)
            and type(capture['registeredAll']) is int
            and capture['registeredAll'] == len(option_names) + len(internal_names), 'Native count mismatch')
    native = provenance.get('nativeInventory', {})
    require(native.get('sha256') == capture['sha256'] and native.get('sizeBytes') == capture['sizeBytes']
            and native.get('options') == len(option_names)
            and native.get('registeredAll') == capture['registeredAll'], 'Capture/provenance mismatch')
    files = records(data['sourceFiles'], 'sourceFiles')
    mods = records(data['sourceMods'], 'sourceMods')
    require('portable-pack.json' in files and any(path.endswith('options.txt') for path in files),
            'Missing descriptor/options source binding')
    require(all(path.startswith('mods/') and path.endswith('.jar') for path in mods), 'Invalid mod source path')
    actual_mods = {path.relative_to(pack).as_posix() for path in (pack / 'mods').rglob('*.jar') if path.is_file()}
    require(actual_mods == set(mods), 'Source JAR namespace changed; capture/review native registry again')
    for name, row in {**files, **mods}.items():
        path = ordinary(pack, name)
        require(path.is_file() and path.stat().st_size == row['sizeBytes'] and sha(path) == row['sha256'],
                'Source input bytes changed: ' + name)
    with (tools / 'registered-keys.tsv').open(encoding='utf-8-sig', newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    registry = [row.get('name') for row in rows]
    require(len(registry) == len(set(registry)) and set(registry) == option_names,
            'TSV namespace differs from native Options')
    require(all('options' in row.get('seen', '').split('+') for row in rows), 'TSV lacks native Options evidence')
    contexts = read(tools / 'contexts.json')
    require(type(contexts) is dict and set(contexts) == option_names, 'Context namespace differs from native Options')
    require(all(type(value) is dict and value.get('context') in {'UNIVERSAL', 'GUI', 'IN_GAME'}
                for value in contexts.values()), 'Unsupported modeled conflict context')
    return {'status': 'PASS', 'options': len(option_names), 'registeredAll': capture['registeredAll'],
            'sourceJars': len(mods), 'sourceFiles': len(files), 'aliasesAdded': 0,
            'snapshotSha256': sha(snapshot_path), 'nativeGameExecuted': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--pack', type=Path, default=HERE.parent.parent)
    args = parser.parse_args()
    try:
        print(json.dumps(validate(args.pack), indent=2))
    except (InvalidRegistry, OSError, ValueError, TypeError, KeyError) as exc:
        parser.exit(1, str(exc) + '\n')


if __name__ == '__main__':
    main()
