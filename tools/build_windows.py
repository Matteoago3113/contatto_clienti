"""Crea un pacchetto portabile Windows con runtime ufficiale verificato.

Uso: python3 tools/build_windows.py RUNTIME.zip SHASUMS256.txt ASAR_CLI
Richiede Node 22+ e @electron/asar 4.3.1. Non installa né disabilita verifiche.
"""
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path
from build_portable import build

VERSION = '44.5.1'
ROOT = Path(__file__).resolve().parents[1]

def package(runtime, sums, asar_cli):
    asset = f'electron-v{VERSION}-win32-x64.zip'
    expected = next(line.split()[0] for line in Path(sums).read_text().splitlines() if line.split()[-1].lstrip('*') == asset)
    with open(runtime, 'rb') as f:
        actual = hashlib.file_digest(f, 'sha256').hexdigest()
    if actual != expected:
        raise ValueError('Checksum SHA-256 del runtime non valido')
    build()
    with tempfile.TemporaryDirectory(prefix='contatto-package-') as tmp:
        stage = Path(tmp) / 'Contatto-Windows'
        app = Path(tmp) / 'app'
        stage.mkdir()
        app.mkdir()
        with zipfile.ZipFile(runtime) as z:
            if any(Path(n).is_absolute() or '..' in Path(n).parts for n in z.namelist()):
                raise ValueError('Percorsi non validi nel runtime')
            z.extractall(stage)
        (stage / 'electron.exe').rename(stage / 'Contatto.exe')
        (stage / 'resources' / 'default_app.asar').unlink(missing_ok=True)
        for name in ['package.json','main.cjs','preload.cjs','catalog-store.cjs']:
            shutil.copy2(ROOT / 'desktop' / name, app / name)
        for name in ['Contatto.html', 'catalog.json']:
            shutil.copy2(ROOT / name, app / name)
        subprocess.run(['node',str(asar_cli),'pack',str(app),str(stage / 'resources' / 'app.asar')],check=True)
        (stage / 'LEGGIMI.txt').write_text('''CONTATTO — WINDOWS 10/11 A 64 BIT

1. Estrai tutta la cartella ZIP sul computer.
2. Apri la cartella Contatto-Windows.
3. Fai doppio clic su Contatto.exe.

Non spostare il solo EXE: deve restare con le DLL e le altre cartelle.
Puoi creare sul Desktop un collegamento a Contatto.exe.
Non servono Python, Node, browser o internet sul tuo computer.

PERCORSO GUIDATO
Nome cliente > Progetto > Email/WhatsApp > Servizio > Messaggio > Bozza.
Sotto il titolo dei modelli trovi l’inizio del testo personalizzato.

GESTISCI MESSAGGI
Il pulsante in alto apre l’archivio: puoi modificare o creare modelli,
salvarli e creare un backup JSON.
I modelli modificati vengono salvati nella cartella dati utente di
Windows, sotto %APPDATA%\\Contatto. Le modifiche precedenti sono
conservate anche in messaggi.json.backup.
I dati del cliente inseriti nella composizione restano nella sessione.
L'app prepara le bozze; non invia email o WhatsApp e non è collegata
al database. Gli allegati vanno aggiunti manualmente.

Questo pacchetto non ha un certificato di firma dell'editore.
Il runtime è verificato contro i checksum della release ufficiale Electron.
''', encoding='utf-8')
        (stage / 'VERSIONE.txt').write_text(f'Contatto 1.0.0\nElectron {VERSION}\nRuntime SHA-256: {actual}\n')
        output = ROOT.parent / 'Contatto-Windows.zip'
        temp_output = Path(tmp) / 'release.zip'
        with zipfile.ZipFile(temp_output,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for p in stage.rglob('*'):
                if p.is_file():
                    z.write(p, str(p.relative_to(stage.parent)))
        shutil.copy2(temp_output, output)
    digest = hashlib.file_digest(open(output,'rb'), 'sha256').hexdigest()
    output.with_suffix('.zip.sha256').write_text(f'{digest}  {output.name}\n')
    print(output)
    return output

if __name__ == '__main__':
    package(*sys.argv[1:4])
