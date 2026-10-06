import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / 'catalog.json').read_text())

    def test_imported_templates_have_traceable_sources(self):
        self.assertEqual(len(self.catalog), 83)
        self.assertEqual(len({t['id'] for t in self.catalog}), 83)
        for t in self.catalog:
            self.assertTrue(t['body'].strip())
            self.assertGreater(t['row'], 0)
            self.assertTrue(t['source'].endswith('.docx'))
            self.assertIn(t['channel'], ('email', 'whatsapp', 'entrambi'))

    def test_variants_are_not_misclassified_as_followups(self):
        variants = [t for t in self.catalog if t['title'] in ('Prima soluzione WhatsApp', 'Seconda soluzione WhatsApp')]
        self.assertEqual(len(variants), 2)
        self.assertTrue(all(t['stage'] == 'primo' for t in variants))
        self.assertFalse(any(t['brand'] == 'Abracadabra' and t['stage'] == 'terzo' for t in self.catalog))

    def test_brand_catalogs_and_personalization(self):
        self.assertEqual({t['brand'] for t in self.catalog}, {'Abracadabra', 'Sitointerattivo'})
        t = next(t for t in self.catalog if t['title'] == 'Dopo incontro · Tu')
        self.assertIn('[Nome]', t['body'])
        self.assertIn('[Azienda]', t['body'])
        self.assertIn('[Descrizione Servizio]', t['body'])

    def test_titles_cover_every_original_and_distinguish_choices(self):
        titles = json.loads((ROOT / 'message-titles.json').read_text())
        self.assertEqual(set(titles), {t['id'] for t in self.catalog})
        groups = {}
        for t in self.catalog:
            title = titles[t['id']]
            self.assertTrue(title.strip())
            self.assertLessEqual(len(title), 90)
            self.assertNotEqual(title, 'Testo')
            for channel in (('email', 'whatsapp') if t['channel'] == 'entrambi' else (t['channel'],)):
                key = (t['brand'], t['category'], channel)
                self.assertNotIn(title, groups.setdefault(key, set()))
                groups[key].add(title)
        self.assertIn('Foto + video', titles['Sitointerattivo-330-None'])
        self.assertIn('dopo telefonata', titles['Sitointerattivo-53-52'])
        self.assertNotIn('Secondo contatto', titles['Abracadabra-2-None'])

    def test_internal_password_rows_not_imported(self):
        self.assertFalse(any(t['sourceLabel'] == 'Password' for t in self.catalog))
        self.assertFalse(any('ciaociao' in t['body'] for t in self.catalog))

if __name__ == '__main__':
    unittest.main()
