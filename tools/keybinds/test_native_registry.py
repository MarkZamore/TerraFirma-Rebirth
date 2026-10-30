"""Publication must reject stale native evidence before accepting a new preset."""
import csv
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

import validate_native_registry as check


class NativeRegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.pack = Path(self.temp.name)
        self.tools = self.pack / 'tools/keybinds'
        self.tools.mkdir(parents=True)
        for name, data in {'portable-pack.json': b'{}\n', 'options.txt': b'lang:en_us\n',
                           'mods/author.jar': b'exact synthetic author bytes'}.items():
            path = self.pack / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        record = lambda name: {'path': name, 'sizeBytes': (self.pack / name).stat().st_size,
                               'sha256': check.sha(self.pack / name)}
        self.data = {'schemaVersion': 1, 'capture': {'sha256': 'a' * 64, 'sizeBytes': 99,
                     'registeredAll': 3, 'options': 2}, 'optionsNames': ['key.a', 'key.b'],
                     'allOnlyNames': ['key.internal'], 'sourceFiles': [record('options.txt'), record('portable-pack.json')],
                     'sourceMods': [record('mods/author.jar')]}
        self.provenance = {'nativeInventory': {'sha256': 'a' * 64, 'sizeBytes': 99, 'registeredAll': 3, 'options': 2}}
        self.pin()
        self.tsv(['key.a', 'key.b'])
        self.write('contexts.json', {name: {'context': 'UNIVERSAL', 'source': 'native'} for name in self.data['optionsNames']})

    def write(self, name, value):
        (self.tools / name).write_text(json.dumps(value), encoding='utf-8')

    def pin(self):
        self.write('native-registry.json', self.data)
        self.provenance['nativeRegistry'] = {'path': 'tools/keybinds/native-registry.json',
                                            'sha256': check.sha(self.tools / 'native-registry.json')}
        self.write('preset-provenance.json', self.provenance)

    def tsv(self, names):
        with (self.tools / 'registered-keys.tsv').open('w', encoding='utf-8', newline='') as stream:
            writer = csv.writer(stream, delimiter='\t')
            writer.writerow(['name', 'seen'])
            writer.writerows((name, 'options') for name in names)

    def reject(self, phrase):
        with self.assertRaisesRegex(check.InvalidRegistry, phrase):
            check.validate(self.pack, self.tools)

    def test_valid_nonproduction_count_is_supported(self):
        self.assertEqual(check.validate(self.pack, self.tools)['options'], 2)

    def test_no_internal_entries_is_valid_for_a_future_capture(self):
        self.data['allOnlyNames'] = []
        self.data['capture']['registeredAll'] = 2
        self.provenance['nativeInventory']['registeredAll'] = 2
        self.pin()
        self.assertEqual(check.validate(self.pack, self.tools)['registeredAll'], 2)

    def test_snapshot_tamper_without_repin_is_rejected(self):
        self.data['optionsNames'][0] = 'key.changed'
        self.write('native-registry.json', self.data)
        self.reject('SHA256 pin')

    def test_missing_native_mapping_is_rejected(self):
        self.tsv(['key.a'])
        self.reject('TSV namespace')

    def test_extra_stale_mapping_is_rejected(self):
        self.tsv(['key.a', 'key.b', 'key.retired'])
        self.reject('TSV namespace')

    def test_context_namespace_drift_is_rejected(self):
        self.write('contexts.json', {'key.a': {'context': 'UNIVERSAL'}})
        self.reject('Context namespace')

    def test_changed_author_jar_is_rejected(self):
        (self.pack / 'mods/author.jar').write_bytes(b'changed author jar')
        self.reject('Source input bytes')

    def test_added_jar_requires_new_native_evidence(self):
        (self.pack / 'mods/new.jar').write_bytes(b'new source mod')
        self.reject('Source JAR namespace')

    def test_changed_author_options_is_rejected(self):
        (self.pack / 'options.txt').write_bytes(b'lang:ru_ru\n')
        self.reject('Source input bytes')

    def test_changed_descriptor_is_rejected(self):
        (self.pack / 'portable-pack.json').write_bytes(b'{"new":true}\n')
        self.reject('Source input bytes')

    def test_duplicate_native_name_is_rejected_even_if_repin_attempted(self):
        self.data['optionsNames'] = ['key.a', 'key.a']
        self.pin()
        self.reject('duplicate names')

    def test_traversal_record_is_rejected_even_if_repin_attempted(self):
        self.data['sourceFiles'][0]['path'] = '../outside'
        self.pin()
        self.reject('Unsafe source path')

    def test_capture_receipt_mismatch_is_rejected(self):
        self.provenance['nativeInventory']['sha256'] = 'b' * 64
        self.write('preset-provenance.json', self.provenance)
        self.reject('Capture/provenance')


if __name__ == '__main__':
    unittest.main()
