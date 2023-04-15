import json
import urllib
from urllib.parse import urlencode
from urllib.request import Request


class Translator:
    __DOMAIN = 'https://mt-auto-minhon-mlt.ucri.jgn-x.jp'

    def __init__(self, client_id: str, client_secret: str, user_name: str):
        self.__client_id = client_id
        self.__user_name = user_name
        self.__access_token = self.__get_access_token(
            client_id=client_id,
            client_secret=client_secret,
        )
        self.__support_languages = self.__get_support_languages()

    @property
    def support_languages(self) -> set[str]:
        return self.__support_languages

    def __get_support_languages(self) -> set[str]:
        url = f'{self.__DOMAIN}/api/mt_standard/get/'
        data = dict(
            key=self.__client_id,
            name=self.__user_name,
            type='json',
            limit=2000,
            access_token=self.__access_token,
        )
        response = json.loads(self.__request(url, data=data))
        return {e['lang_s'] for e in response['resultset']['result']['list']}

    def translate_text(self, text: str, source_lang: str, target_lang: str) -> str:
        self.__check(text, source_lang, target_lang)

        data = dict(
            key=self.__client_id,
            name=self.__user_name,
            type='json',
            access_token=self.__access_token,
            text=text,
        )
        url = f'{self.__DOMAIN}/api/mt/generalNT_{source_lang}_{target_lang}/'
        response = json.loads(self.__request(url, data=data))
        return response['resultset']['result']['text']

    def __check(self, text: str, source_lang: str, target_lang: str):
        if not self.__exist_lang(source_lang):
            raise ValueError(f'doesn\'t exist source_lang: {source_lang}')
        if not self.__exist_lang(target_lang):
            raise ValueError(f'doesn\'t exist target_lang: {target_lang}')
        if text is None or text == '':
            raise ValueError('doesn\'t exist text')

    def __exist_lang(self, lang: str):
        return lang in self.support_languages

    @classmethod
    def __get_access_token(cls, client_id: str, client_secret: str) -> str:
        client_data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
        }
        url = f'{cls.__DOMAIN}/oauth2/token.php'
        response = json.loads(cls.__request(url, data=client_data))
        return response['access_token']

    @staticmethod
    def __request(url: str, data: dict[str, str]) -> str:
        request_object = Request(url, urlencode(data).encode('ascii'), method='POST')

        with urllib.request.urlopen(request_object) as response:
            return response.read().decode('utf-8')
