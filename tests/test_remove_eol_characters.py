from pre_commit_hooks.remove_eol_characters import remove_eol, rewrite_file

original_text = """这是一个，
测试。
This is a
test
"""
rewrote_text = """这是一个，测试。
This is a
test
"""


def test_remove_eol_characters(tmp_path):
    file_path = str(tmp_path / 'test.md')
    with open(file_path, mode='w', encoding='utf-8') as f:
        f.write(original_text)
    strategies = [remove_eol()]
    assert rewrite_file(file_path, strategies)
    with open(file_path, encoding='utf-8') as f:
        contents = f.read()
    assert contents == rewrote_text
