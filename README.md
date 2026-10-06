# Contatto clienti — fase 1

App italiana con percorso guidato, una schermata alla volta: dati del cliente → Sitointerattivo/Abracadabra → email/WhatsApp → servizio → messaggio dalle etichette della colonna sinistra del Word → bozza precompilata. Le scelte sono obbligatorie; i campi aggiuntivi dipendono dal messaggio scelto. Personalizza, modifica e copia o scarica la bozza in formato TXT. Tornando indietro senza cambiare dati o modello, le modifiche manuali alla bozza vengono conservate.

## Programma Windows

Il pacchetto `Contatto-Windows.zip` contiene un programma portabile per Windows 10/11 a 64 bit. Estrai tutta la cartella e apri `Contatto.exe`; conserva DLL e cartelle accanto all’eseguibile. Non servono installazioni aggiuntive. Puoi creare un collegamento sul Desktop.

Il pulsante **Gestisci messaggi** consente di modificare testi, titoli, ambiti, canali e fasi, oppure aggiungere modelli. I modelli vengono salvati in `%APPDATA%\Contatto\messaggi.json`, con una copia precedente in `.backup`. Il pulsante Backup messaggi esporta l’archivio JSON. I dati del cliente restano nella sessione, mentre il catalogo modificato persiste. Questa versione non invia messaggi.

La versione desktop usa Electron 44.5.1 con isolamento del renderer e API limitate al catalogo. Il runtime Windows è verificato con SHA-256 dalla release ufficiale. Il pacchetto dell’app non dispone di certificato dell’editore; l’avvio Windows non è stato verificato su questa macchina Linux.

Per ricostruire il pacchetto: scarica `electron-v44.5.1-win32-x64.zip` e `SHASUMS256.txt` dalla release ufficiale, installa `@electron/asar@4.3.1` in una cartella di strumenti e usa `python3 tools/build_windows.py RUNTIME.zip SHASUMS256.txt /percorso/asar.mjs`. Il build rigenera Contatto.html, verifica il checksum e include soltanto i file necessari. Test del salvataggio: `node --test tests/catalog-store.test.cjs`.

## App pronta da aprire

Apri `Contatto.html` con doppio clic in Chrome, Edge, Firefox o Safari: contiene interfaccia e catalogo, funziona offline e non richiede installazioni o server. Per rigenerare il file dopo modifiche esegui `python3 tools/build_portable.py`. Per inviare i messaggi usa il tuo programma email o WhatsApp.

## Avvio per sviluppo

Richiede Python 3 e un browser moderno. Nessuna dipendenza da installare.

```sh
cd /workspace/contatto_clienti
python3 server.py
```

Il server di sviluppo usa la porta 8000 sull'interfaccia locale. Non è un server di produzione. Nessun messaggio viene inviato: la fase 1 prepara il testo. Nessun collegamento al database è implementato e nessun dato personale è salvato in modo persistente. Le modifiche manuali vengono sostituite quando cambiano il modello o i campi personali. Il pulsante Nuovo messaggio azzera i dati della compilazione.

## Contenuti

`catalog.json` contiene 83 modelli selezionati dai due Word forniti, con riferimento al documento, etichetta originale e riga della tabella. Le password incorporate sono sostituite dal campo [Password demo]. I testi e gli oggetti rimangono per il resto quelli delle fonti, con collegamenti esterni di Word riportati nel testo dove disponibili. Il formato visuale del Word non è riprodotto. La variante WhatsApp di invio presentazione Abracadabra comprende anche i link del paragrafo seguente.

Le fasi sono classificazioni operative: primo contatto, seguito a incontro/telefonata, promemoria, servizi. Le due “soluzioni WhatsApp” iniziali di Abracadabra sono varianti del primo contatto. I documenti non contengono un terzo contatto per ogni ambito: l'interfaccia mostra l'assenza del modello senza generarne uno. È presente un promemoria del percorso formativo Sitointerattivo; nessun terzo contatto Abracadabra è stato inventato.

Note interne, password, percorsi locali, contratti, listini e schede annullate non sono importati come modelli autonomi. I riferimenti ad allegati all'interno dei messaggi sono mantenuti: i file non sono allegati automaticamente. Date, prezzi e affermazioni commerciali contenute nei testi vanno verificati dall'operatore. Ambiti con soli collegamenti o senza testo (per esempio Social media) non hanno modelli dedicati.

Per rigenerare il catalogo dai Word:

```sh
python3 tools/import_documents.py '/percorso/SIA.docx' '/percorso/MM.docx'
```

La selezione delle righe è esplicita in `tools/import_documents.py`: se i Word cambiano struttura, aggiornarla e verificare il catalogo.

## Verifica

```sh
python3 -m unittest discover -s tests -v
node --check app.js
```

La futura fase 2 potrà valorizzare i campi dal database e integrare invio e storico. Questa versione non richiede credenziali né servizi esterni.
