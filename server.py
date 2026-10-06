"""Server locale per lo sviluppo: nessun invio email o WhatsApp."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    handler = partial(SimpleHTTPRequestHandler, directory=str(root))
    with ThreadingHTTPServer(('127.0.0.1', 8000), handler) as server:
        print('Contatto avviato sulla porta 8000', flush=True)
        server.serve_forever()
