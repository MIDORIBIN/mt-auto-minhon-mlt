import os
from unittest import TestCase

from src.mt_auto_minhon_mlt import Translator


class TestTranslator(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.translator = Translator(
            client_id=os.environ['client_id'],
            client_secret=os.environ['client_secret'],
            user_name=os.environ['user_name'],
        )

    def test_support_languages(self):
        expected = {'en', 'lo', 'ko', 'ne', 'th', 'fp', 'es', 'km', 'it', 'vi', 'de', 'zh-CN', 'fr', 'ur', 'ru', 'pt',
                    'tr', 'nl', 'ar', 'si', 'hi', 'my', 'uk', 'id', 'pt-BR', 'mn', 'da', 'ja', 'hu', 'ms', 'zh-TW',
                    'pl'}
        self.assertEqual(expected, self.translator.support_languages)

    def test_translate_text(self):
        jp_text = 'みんなの自動翻訳'
        en_expected = 'Minna no Jido Hon\''
        en_actual = self.translator.translate_text(jp_text, source_lang='ja', target_lang='en')
        self.assertEqual(en_expected, en_actual)

        en_text = 'Minna no Automatic translation'
        jp_expected = 'みんなの自動翻訳'
        jp_actual = self.translator.translate_text(en_text, source_lang='en', target_lang='ja')
        self.assertEqual(jp_expected, jp_actual)
