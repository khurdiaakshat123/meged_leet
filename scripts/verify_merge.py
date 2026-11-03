"""Verify the merged bank against its provenance and, optionally, source ZIPs.

Usage: python scripts/verify_merge.py [--sources]
The optional flag expects the original four ZIPs in mergeall's parent folder.
Uses only the Python standard library and never modifies question files.
"""
import collections
import hashlib
import json
import pathlib
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent

def file_hash(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def main():
    manifest = json.loads((ROOT/'manifests/merge-provenance.json').read_text(encoding='utf-8'))
    index = json.loads((ROOT/'manifests/questions-index.json').read_text(encoding='utf-8'))
    errors, paths, questions = [], set(), set()
    source_zips = {}
    counts = collections.Counter()
    for r in manifest['files']:
        rel = r['path']
        p = ROOT / rel
        if not p.resolve().is_relative_to((ROOT/'questions').resolve()):
            errors.append(f'Invalid provenance path: {rel}')
            continue
        if rel in paths:
            errors.append(f'Duplicate provenance path: {rel}')
        paths.add(rel)
        parts = pathlib.PurePosixPath(rel).parts
        expected = manifest['topicOwners'][parts[2]] if parts[1] == 'dsa' else 'rishi'
        if r['contributor'] != expected or r['archive'] != expected+'_leet.zip':
            errors.append(f'Topic source mismatch: {rel}')
        if not p.is_file() or file_hash(p) != r['sha256']:
            errors.append(f'Missing or changed file: {rel}')
        if rel.endswith('.json'):
            questions.add(rel)
            for field in ('testCases', 'publicTests', 'examples'):
                counts[field] += r[field]
            for ref in r.get('localImageReferences', []):
                from urllib.parse import unquote
                if not (p.parent/unquote(ref)).is_file():
                    errors.append(f'Missing image: {rel}: {ref}')
        if '--sources' in sys.argv:
            archive = r['archive']
            if archive not in source_zips:
                source_zips[archive] = zipfile.ZipFile(ROOT.parent/archive)
            raw = source_zips[archive].read(r['archivePath'])
            if hashlib.sha256(raw).hexdigest() != r['sha256']:
                errors.append(f'Original source mismatch: {rel}')
    disk = {p.relative_to(ROOT).as_posix() for p in (ROOT/'questions').rglob('*') if p.is_file()}
    if disk != paths:
        errors.append(f'File inventory mismatch: missing={sorted(paths-disk)}, extra={sorted(disk-paths)}')
    index_paths = [e['path'] for e in index['questions']]
    if set(index_paths) != questions or len(index_paths) != len(questions) or index['totalQuestions'] != len(questions):
        errors.append('Question index mismatch')
    for z in source_zips.values():
        z.close()
    print(json.dumps({'status':'PASS' if not errors else 'FAIL',
                      'verifiedFiles':len(paths), 'questions':len(questions),
                      'assets':len(paths)-len(questions), **counts,
                      'comparedWithOriginalZips':'--sources' in sys.argv,
                      'errors':errors}, indent=2))
    return bool(errors)

if __name__ == '__main__':
    sys.exit(main())
