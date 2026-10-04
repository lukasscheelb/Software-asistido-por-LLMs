import hashlib,json,subprocess,tomllib
from pathlib import Path

def test_must_chain_paths_tests_stories_hashes_and_commits_exist():
    root=Path(__file__).resolve().parents[1]
    matrix=json.loads((root/'docs/qa/traceability.json').read_text(encoding='utf-8'))
    git=['git','-c',f'safe.directory={root.as_posix()}']
    assert len(matrix['requirements']) == 22
    for row in matrix['requirements']:
        for path in row['artifacts']+[row['code'],row['test']]: assert (root/path).is_file(),path
        tickets=tomllib.loads((root/row['story_file']).read_text(encoding='utf-8'))
        assert any(entry['id']==row['story_id'] for entry in tickets['entry'])
        assert row['test_name'] in (root/row['test']).read_text(encoding='utf-8')
        for path in (row['code'],row['test']):
            data=subprocess.check_output(git+['show',row['commit']+':'+path],cwd=root)
            assert hashlib.sha256(data).hexdigest()==row['hashes'][path]
