import json
import os
import urllib
from urllib.parse import urlencode
from urllib.request import Request


def main():
    response = get_list()
    support_languages = response['resultset']['result']['list']
    support_languages = [[e['id'].split('_')[0], e['lang_s'], e['lang_t']] for e in support_languages]

    with open('../src/mt_auto_minhon_mlt/assets/support_translate.json', encoding='utf-8', mode='w') as f:
        json.dump(support_languages, f, indent=2)


def get_list() -> dict:
    url = f'https://mt-auto-minhon-mlt.ucri.jgn-x.jp/api/mt_standard/get/'

    client_id = os.environ['client_id']
    client_secret = os.environ['client_secret']
    user_name = os.environ['user_name']

    request_data = dict(
        key=client_id,
        name=user_name,
        type='json',
        limit=2000,
        access_token=get_access_token(client_id, client_secret),
    )

    request_object = Request(url, urlencode(request_data).encode('ascii'), method='POST')

    with urllib.request.urlopen(request_object) as res:
        response = res.read().decode('utf-8')
    return json.loads(response)


def get_access_token(client_id: str, client_secret: str) -> str:
    url = f'https://mt-auto-minhon-mlt.ucri.jgn-x.jp/oauth2/token.php'
    client_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    }
    request_object = Request(url, urlencode(client_data).encode('ascii'), method='POST')

    with urllib.request.urlopen(request_object) as response:
        response_body = response.read().decode('utf-8')
    return json.loads(response_body)['access_token']


if __name__ == '__main__':
    main()
