"""Importazione dei testi selezionati dai Word originali, senza eseguire istruzioni."""
import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
R = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'

def rows(path):
    with zipfile.ZipFile(path) as z:
        rel = ET.fromstring(z.read('word/_rels/document.xml.rels'))
        links = {x.attrib['Id']: x.attrib['Target'] for x in rel if x.attrib.get('TargetMode') == 'External'}
        root = ET.fromstring(z.read('word/document.xml'))
    result = []
    for row in root.findall('.//w:tr', NS):
        cells = []
        for cell in row.findall('w:tc', NS):
            paragraphs = []
            for p in cell.findall('.//w:p', NS):
                text = ''.join(x.text or '' for x in p.findall('.//w:t', NS))
                for h in p.findall('.//w:hyperlink', NS):
                    url = links.get(h.attrib.get(R), '')
                    if url.startswith(('https://', 'http://')) and url not in text:
                        text += ' (' + url + ')'
                paragraphs.append(text)
            cells.append('\n'.join(paragraphs).strip())
        result.append(cells)
    return result

# (riga testo, riga oggetto, ambito, canale, fase, nome leggibile)
SIA = [
(17,16,'Presentazione aziendale','email','secondo','Presentazione servizi'),
(18,None,'Presentazione aziendale','whatsapp','secondo','Presentazione servizi'),
(19,None,'Presentazione aziendale','entrambi','servizi','Learning, eventi e marketing'),
(25,16,'Presentazione aziendale','email','secondo','Dopo incontro · Tu'),
(26,16,'Presentazione aziendale','email','secondo','Dopo incontro · Lei'),
(35,33,'Presentazione aziendale','email','primo','Richiesta di incontro · Istituzionale'),
(35,34,'Presentazione aziendale','email','primo','Richiesta di incontro · Friendly'),
(48,47,'Presentazione aziendale','email','primo','Presentazione ai commerciali'),
(22,None,'Presentazione aziendale','email','secondo','Accordo di riservatezza'),
(27,None,'Presentazione aziendale','email','primo','Lettera di presentazione GBG'),
(53,52,'Streaming','email','secondo','Dopo telefonata · Tu'),
(54,52,'Streaming','email','secondo','Dopo telefonata · Lei'),
(58,57,'Streaming','email','secondo','Presentazione da Ilenia'),
(62,61,'Streaming','email','secondo','Presentazione ad agenzie pubblicitarie'),
(65,64,'Streaming','email','servizi','Invito evento Studio BNC'),
(68,None,'Streaming','entrambi','servizi','Presentazione streaming'),
(71,70,'Webinar','email','servizi','Link evento Studio BNC'),
(72,None,'Webinar','whatsapp','servizi','Link evento Studio BNC'),
(106,None,'Webinar','entrambi','servizi','Piattaforma webinar demo'),
(195,194,'Servizi informatica','email','secondo','Manutenzione · Personalizzato'),
(196,194,'Servizi informatica','email','servizi','Manutenzione · Spiegazione generale'),
(200,199,'Servizi informatica','email','servizi','Cybersecurity e NIS2'),
(203,202,'Servizi informatica','email','servizi','Intelligenza artificiale'),
(211,210,'Corsi','email','servizi','Formazione in omaggio'),
(232,None,'Coaching – Counseling','email','secondo','Preparazione incontro'),
(234,None,'Coaching – Counseling','email','servizi','Collaborazione nella formazione'),
(236,None,'Ipnosi','email','secondo','Dopo incontro'),
(252,251,'Ipnosi','email','servizi','Ipnosi e sport'),
(253,251,'Ipnosi','email','servizi','Ipnosi e sport · Versione 2'),
(280,279,'Team - Group building','email','secondo','Presentazione dopo telefonata'),
(287,286,'Team - Group building','email','servizi','Se ne ride chi abita i cieli'),
(288,None,'Team - Group building','email','servizi','Iscrizione e pagamento'),
(291,None,'Team - Group building','email','terzo','Promemoria evento'),
(293,292,'Team - Group building','email','servizi','Invito al percorso formativo'),
(297,296,'Team - Group building','email','servizi','Azionabile'),
(302,301,'Team - Group building','email','servizi','Affidarsi e Fidarsi'),
(305,304,'Team - Group building','email','servizi','Prestigi DiVini'),
(309,307,'Team - Group building','email','servizi','Tre team building'),
(310,308,'Team - Group building','entrambi','servizi','Tre team building · Sintetico'),
(314,None,'Web e-commerce','email','servizi','Esempi e-commerce'),
(315,None,'Web e-commerce','entrambi','servizi','Software WhatsApp'),
(28,None,'Comunicazione integrata','email','servizi','Partner strategico'),
(29,None,'Comunicazione integrata','email','servizi','Partner strategico · Sintetico'),
(30,None,'Comunicazione integrata','entrambi','servizi','Presentazione alternativa'),
(323,None,'Grafica','email','servizi','Comunicazione integrata e grafica'),
(330,None,'Consegna materiale digitale','email','servizi','Consegna e ringraziamento'),
(331,None,'Ringraziamento per CV ricevuto','email','servizi','Risposta al curriculum'),
(337,None,'WOW','entrambi','servizi','Presentazione WOW.CONTACT'),
(338,None,'WOW','entrambi','secondo','Prova della piattaforma'),
(348,346,'Rassegna stampa','email','servizi','Presentazione informale'),
(350,349,'Rassegna stampa','email','servizi','Presentazione formale'),
(352,351,'Rassegna stampa','email','secondo','Proposta demo per associazioni'),
(358,357,'Terzo tempo sport magazine','email','servizi','Presentazione generale'),
(362,361,'Terzo tempo sport magazine','email','servizi','Sponsorizzazione'),
(402,401,'Streaming','email','servizi','Matrimonio in streaming'),
]
MM = [
(1,None,'Presentazione Spettacoli','whatsapp','primo','Prima soluzione WhatsApp'),
(2,None,'Presentazione Spettacoli','whatsapp','primo','Seconda soluzione WhatsApp'),
(4,None,'Presentazione Spettacoli','whatsapp','primo','Presentazione con note'),
(5,None,'Presentazione Spettacoli','whatsapp','secondo','Invio presentazione magica'),
(17,16,'Clienti aziendali','email','servizi','Cena aziendale'),
(18,None,'Clienti aziendali','whatsapp','servizi','Cena aziendale'),
(19,None,'Ristoranti e organizzatori','entrambi','primo','Proposta informale'),
(20,None,'Ristoranti e organizzatori','whatsapp','primo','Proposta informale breve'),
(24,22,'Presentazione Spettacoli','email','primo','Offri emozioni'),
(27,26,'Presentazione Spettacoli','email','primo','Presentazione illusionista'),
(28,26,'Presentazione Spettacoli','email','secondo','Invio presentazione promessa'),
(31,30,'Possibili partner','email','primo','Proposta di collaborazione'),
(36,35,'Location per matrimoni ed eventi aziendali','email','primo','Collaborazione con location'),
(39,38,'Presentazione Ivano Berlendis','email','servizi','Arte e magia'),
(42,41,'Sposi conosciuti in fiera','email','secondo','Proposta matrimonio'),
(45,44,'Bergamo Sposi','email','servizi','Presentazione matrimonio'),
(48,47,'Ristoranti e organizzatori','email','secondo','Dopo incontro al ristorante'),
(51,50,'Risposta Prontopro','email','secondo','Ringraziamento'),
(54,53,'Wedding professional','email','primo','Presentazione wedding'),
(57,56,'Presentazione post telefonata/contatto','email','secondo','Eventi magici e team building'),
(143,142,'Prestigi DiVini','email','servizi','Spettacolo e team building'),
(146,142,'Prestigi DiVini','entrambi','servizi','Supporto al vostro evento'),
(154,None,'Autonoleggio','email','servizi','Auto per matrimoni'),
(171,None,'Videoperatori','email','servizi','Servizio video matrimonio'),
(177,None,'Presentazione post telefonata/contatto','whatsapp','secondo','Dopo cena di gala'),
(178,None,'Presentazione post telefonata/contatto','whatsapp','secondo','Invio presentazione promessa'),
(181,None,'Presentazione Spettacoli','whatsapp','primo','Proposta di call o incontro'),
(184,None,'Clienti aziendali','whatsapp','servizi','Cena aziendale · Versione GB'),
]

def generate(sia, mm):
    result = []
    for brand, path, mapping in [('Sitointerattivo', sia, SIA), ('Abracadabra', mm, MM)]:
        source = rows(path)
        for i, subject, category, channel, stage, title in mapping:
            text = re.sub(r'(password è )\S+', r'\1[Password demo]', source[i][1], flags=re.IGNORECASE)
            if brand == 'Abracadabra' and i == 178:
                text += '\n\n' + source[179][1]
            result.append(dict(id=f'{brand}-{i}-{subject}',brand=brand,category=category,channel=channel,stage=stage,title=title,body=text,subject=source[subject][1] if subject is not None else '',source=Path(path).name,sourceLabel=source[i][0] or title,row=i+1))
    return result

if __name__ == '__main__':
    Path('catalog.json').write_text(json.dumps(generate(*sys.argv[1:3]),ensure_ascii=False,indent=2)+'\n')
