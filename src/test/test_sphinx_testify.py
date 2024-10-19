import pytest


@pytest.mark.sphinx('html', testroot='single-passed-test')
def test_one_successful_test_rendered_to_html_comments(app):
    app.build(filenames=[app.srcdir / 'index.rst'])
    html = (app.outdir / 'index.html').read_text(encoding='utf8')
    assert '<!-- hello world -->' in html
