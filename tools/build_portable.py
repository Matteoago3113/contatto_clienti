"""Genera un'app HTML autonoma, apribile con doppio clic e senza server."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def build():
    html = (ROOT / 'index.html').read_text()
    css = (ROOT / 'style.css').read_text()
    js = (ROOT / 'app.js').read_text()
    titles = json.loads((ROOT / 'message-titles.json').read_text())
    catalog = json.loads((ROOT / 'catalog.json').read_text())
    metadata = {t['id']: {'title': titles[t['id']], 'originalLabel': t['sourceLabel']} for t in catalog}
    titles_js = 'window.contattoMessageTitles = ' + json.dumps(metadata, ensure_ascii=False).replace('<', chr(92) + 'u003c') + ';'
    (ROOT / 'message-titles.js').write_text(titles_js)
    data = json.dumps(json.loads((ROOT / 'catalog.json').read_text()), ensure_ascii=False)
    data = data.replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    html = html.replace('<link rel="stylesheet" href="style.css">', '<style>' + css + '</style>')
    html = html.replace('<script src="app.js" defer></script>', '')
    html = html.replace('<script src="message-titles.js" defer></script>', '<script>' + titles_js + '</script>')
    html = html.replace('<a class="logo" href="./">', '<a class="logo" href="#">')
    html = html.replace('</body>', '<script id="embedded-catalog" type="application/json">' + data + '</script><script>' + js + '</script></body>')
    target = ROOT / 'Contatto.html'
    target.write_text(html)
    return target

if __name__ == '__main__':
    print(build())
