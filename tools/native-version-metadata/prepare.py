"""Prepare pack-owned, code-free native version metadata from a verified client.

No Minecraft version table or runtime mod detection. Author game/mod JARs stay intact.
"""
from __future__ import annotations
import argparse,copy,hashlib,io,json,os,re,tempfile,zipfile
from pathlib import Path

OUTPUT='config/native-version-metadata.jar'
FLAGS='launcher/jvm-args.txt'
OWNED='launcher/pack-owned.txt'
STATE='tools/native-version-metadata/ownership.json'
FLAG='-Xbootclasspath/a:'+OUTPUT
KIND='native-version-resource-projection'
LIMIT=65536

def sha(data):return hashlib.sha256(data).hexdigest()
def digest(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def json_bytes(value):return (json.dumps(value,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
def safe(root,relative):
    if not isinstance(relative,str) or not relative or relative.startswith('/') or ':' in relative or '\\' in relative or any(part in {'','.','..'} for part in relative.split('/')):
        raise ValueError('Unsafe source/output path')
    path=root.joinpath(*relative.split('/'))
    if not path.resolve().is_relative_to(root.resolve()):raise ValueError('Path escaped source tree')
    for current in [path,*path.parents]:
        if current.exists() and (current.is_symlink() or getattr(current.lstat(),'st_file_attributes',0)&0x400):raise ValueError('Linked source/output path refused')
        if current==root:break
    return path
def unique_object(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError('Duplicate native metadata property')
        result[key]=value
    return result
def archive_metadata(client,expected_id):
    with zipfile.ZipFile(client) as archive:
        rows=[row for row in archive.infolist() if row.filename=='version.json']
        if not rows:return None,None
        if len(rows)!=1 or rows[0].file_size>LIMIT:raise ValueError('Ambiguous/oversized native version metadata')
        with archive.open(rows[0]) as stream:raw=stream.read(LIMIT+1)
    if len(raw)>LIMIT:raise ValueError('Native metadata exceeds its bound')
    metadata=json.loads(raw.decode('utf-8-sig'),object_pairs_hook=unique_object)
    if not isinstance(metadata,dict) or metadata.get('id')!=expected_id:raise ValueError('Native Minecraft ID differs from portable descriptor')
    for field in ('protocol_version','world_version'):
        value=metadata.get(field)
        if type(value) is not int or not 0<=value<=2147483647:raise ValueError('Invalid native integer '+field)
    return raw,metadata
def resource_jar(raw):
    buffer=io.BytesIO()
    with zipfile.ZipFile(buffer,'w') as archive:
        entry=zipfile.ZipInfo('version.json',(1980,1,1,0,0,0));entry.create_system=0;entry.external_attr=0x20
        entry.compress_type=zipfile.ZIP_STORED;archive.writestr(entry,raw)
    result=buffer.getvalue()
    with zipfile.ZipFile(io.BytesIO(result)) as archive:
        if archive.namelist()!=['version.json'] or archive.read('version.json')!=raw:raise ValueError('Projection is not exact native metadata only')
    return result
def append_line(raw,line):
    lines=raw.decode('utf-8-sig').splitlines()
    count=sum(value.strip()==line for value in lines)
    if count>1:raise ValueError('Duplicate managed data line')
    if count:return raw
    newline=b'\r\n' if b'\r\n' in raw else b'\n'
    return raw+(b'' if not raw or raw.endswith(b'\n') else newline)+line.encode('utf-8')+newline
def remove_line(raw,line):
    bom=raw.startswith(b'\xef\xbb\xbf')
    text=''.join(value for value in raw.decode('utf-8-sig').splitlines(keepends=True) if value.strip()!=line)
    return (b'\xef\xbb\xbf' if bom and text else b'')+text.encode('utf-8')
def read_optional(root,path):
    target=safe(root,path);return target.read_bytes() if target.is_file() else b''

def prepare(root,lock_relative='tools/upstream-lock.json'):
    root=root.absolute()
    if (root/'saves').exists() or (root/'logs/latest.log').exists():raise ValueError('Source preparation refuses a personal/live game instance')
    descriptor=json.loads(safe(root,'portable-pack.json').read_text(encoding='utf-8-sig'))
    client_relative=descriptor.get('clientJar');client=safe(root,client_relative)
    expected_id=descriptor.get('minecraftVersion')
    if not isinstance(expected_id,str) or not expected_id:raise ValueError('Missing native Minecraft descriptor ID')
    lock_path=safe(root,lock_relative);original_lock=json.loads(lock_path.read_text(encoding='utf-8-sig'))
    lock=copy.deepcopy(original_lock)
    support=lock.get('supportFiles',[])
    if not isinstance(support,list) or len({row['path'].casefold() for row in support})!=len(support):raise ValueError('Duplicate/invalid support-file pins')
    pins=[row for row in support if row.get('path')==client_relative]
    if len(pins)!=1 or not re.fullmatch('[a-fA-F0-9]{64}',pins[0].get('sha256','')) or type(pins[0].get('sizeBytes')) is not int or pins[0]['sizeBytes']<=0:
        raise ValueError('Client needs one independently verified source size/SHA256 pin')
    source_hash=digest(client)
    if source_hash!=pins[0]['sha256'].lower() or client.stat().st_size!=pins[0].get('sizeBytes'):raise ValueError('Client bytes differ from verified source pin')
    raw,metadata=archive_metadata(client,expected_id)
    if digest(client)!=source_hash:raise ValueError('Client changed while reading native metadata')
    state_path=safe(root,STATE)
    previous=json.loads(state_path.read_text(encoding='utf-8-sig')) if state_path.is_file() else None
    if previous and (previous.get('schemaVersion')!=1 or previous.get('kind')!=KIND):raise ValueError('Unknown projection ownership schema')
    existing=read_optional(root,OUTPUT)
    projected=resource_jar(raw) if raw is not None else None
    if existing and sha(existing)!=(previous or {}).get('outputSha256') and (projected is None or existing!=projected):
        raise ValueError('Unowned/edited metadata output; preserve source bytes for review')
    flags=read_optional(root,FLAGS);owned=read_optional(root,OWNED)
    plans={}
    if projected is not None:
        plans.update({OUTPUT:projected,FLAGS:append_line(flags,FLAG),OWNED:append_line(owned,OUTPUT)})
    elif previous:
        plans.update({OUTPUT:None,FLAGS:remove_line(flags,FLAG),OWNED:remove_line(owned,OUTPUT)})
    state={'schemaVersion':1,'kind':KIND,'sourceClient':{'path':client_relative,'sizeBytes':client.stat().st_size,'sha256':source_hash},
        'minecraftVersion':expected_id,'enabled':projected is not None,'metadataSha256':sha(raw) if raw is not None else None,
        'metadataBytes':len(raw) if raw is not None else None,'protocolVersion':metadata['protocol_version'] if metadata else None,
        'worldVersion':metadata['world_version'] if metadata else None,'outputPath':OUTPUT,'outputSha256':sha(projected) if projected is not None else None,
        'outputEntries':['version.json'] if projected is not None else [],'classEntries':0,'managedJvmFlag':FLAG,'managedOwnedPattern':OUTPUT}
    if projected is not None or previous:plans[STATE]=json_bytes(state)
    managed={OUTPUT,FLAGS,OWNED}
    updated=[];seen=set()
    for row in support:
        relative=row['path']
        if relative not in managed:updated.append(row);continue
        value=plans.get(relative,read_optional(root,relative))
        if value is not None:updated.append({**row,'sizeBytes':len(value),'sha256':sha(value)})
        seen.add(relative)
    for relative in sorted(set(plans)&managed-seen):
        value=plans[relative]
        if value is not None:updated.append({'path':relative,'sizeBytes':len(value),'sha256':sha(value)})
    lock['supportFiles']=updated
    if projected is not None or previous:plans[lock_relative]=json_bytes(lock)
    if any(original_lock.get(key)!=lock.get(key) for key in set(original_lock)|set(lock) if key!='supportFiles'):
        raise ValueError('Preparation changed non-support lock fields')
    if [row for row in support if row['path'] not in managed]!=[row for row in updated if row['path'] not in managed]:raise ValueError('Preparation changed unrelated support pins')
    report={**state,'status':'PREPARED_NATIVE_METADATA' if projected is not None else 'NO_NATIVE_METADATA',
        'gameOrAuthorModJarsChanged':False,'clientSourceUnchanged':True,'gameInstanceModified':False,
        'futureVersionTableOrJarCountGate':False,'onlySupportFilePinsUpdated':sorted(set(plans)&managed),
        'changedPaths':[path for path,value in plans.items() if (safe(root,path).read_bytes() if safe(root,path).is_file() else None)!=value]}
    return plans,report

def atomic(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    temporary=None
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent,prefix='.native-metadata-',delete=False) as stream:
            temporary=Path(stream.name);stream.write(data);stream.flush();os.fsync(stream.fileno())
        os.replace(temporary,path);temporary=None
    finally:
        if temporary is not None:temporary.unlink(missing_ok=True)
def apply(root,plans):
    paths={relative:safe(root,relative) for relative in plans}
    before={relative:path.read_bytes() if path.is_file() else None for relative,path in paths.items()}
    changed=[]
    try:
        for relative,value in plans.items():
            if before[relative]==value:continue
            path=paths[relative]
            if value is None:path.unlink(missing_ok=True)
            else:atomic(path,value)
            changed.append(relative)
    except Exception as error:
        failures=[]
        for relative in reversed(changed):
            try:
                if before[relative] is None:paths[relative].unlink(missing_ok=True)
                else:atomic(paths[relative],before[relative])
            except Exception as failure:failures.append(str(failure))
        if failures:raise RuntimeError('Source rollback needs review: '+str(failures)) from error
        raise
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--pack',required=True,type=Path)
    parser.add_argument('--source-lock',default='tools/upstream-lock.json');parser.add_argument('--report',type=Path)
    mode=parser.add_mutually_exclusive_group();mode.add_argument('--apply',action='store_true');mode.add_argument('--check',action='store_true')
    args=parser.parse_args();root=args.pack.resolve(strict=True)
    plans,report=prepare(root,args.source_lock)
    report_relative=None
    if args.report:
        report_path=(args.report if args.report.is_absolute() else root/args.report).resolve()
        report_relative=report_path.relative_to(root).as_posix()
        if not report_relative.startswith('tools/'):raise ValueError('Preparation report must remain source-only under tools/')
        safe(root,report_relative)
    if args.check and report['changedPaths']:raise ValueError('Generated native metadata is stale: '+', '.join(report['changedPaths']))
    if args.apply:
        if report_relative:plans[report_relative]=json_bytes(report)
        apply(root,plans)
    elif report_relative and not args.check:atomic(safe(root,report_relative),json_bytes(report))
    print(json.dumps({'status':report['status'],'minecraftVersion':report['minecraftVersion'],'protocolVersion':report['protocolVersion'],
        'metadataBytes':report['metadataBytes'],'classEntries':0,'changedPaths':report['changedPaths']},ensure_ascii=False))
if __name__=='__main__':main()
