import datetime, base64, requests, json
from Crypto.Hash import CMAC
from Crypto.Cipher import AES

secret_key = '2ebc2c087c1501480834538ff72139bc'
api_key = 'SrSOEY9mBe6Ndl7bwyVPs5TsTPFTEq9tra8Occad'

def lock(uuid: str):
    base64_history = get_history_base64('web lock')
    headers = get_header()
    sign = get_sign()

    url = f'https://app.candyhouse.co/api/sesame2/{uuid}/cmd'
    body = {
        'cmd': 82,
        'history': base64_history,
        'sign': sign
    }

    res = requests.post(url, json.dumps(body), headers=headers)
    print(res.status_code, res.text)


def unlock(uuid: str):
    base64_history = get_history_base64('web unlock')
    headers = get_header()
    sign = get_sign()

    url = f'https://app.candyhouse.co/api/sesame2/{uuid}/cmd'
    body = {
        'cmd': 83,
        'history': base64_history,
        'sign': sign
    }
    res = requests.post(url, json.dumps(body), headers=headers)
    print(res.status_code, res.text)


def get_history_base64(history: str):
    base64_history = base64.b64encode(bytes(history, 'utf-8')).decode()
    return base64_history


def get_sign():

    cmac = CMAC.new(bytes.fromhex(secret_key), ciphermod=AES)
    ts = int(datetime.datetime.now().timestamp())
    message = ts.to_bytes(4, byteorder='little')
    message = message.hex()[2:8]
    cmac = CMAC.new(bytes.fromhex(secret_key), ciphermod=AES)
    cmac.update(bytes.fromhex(message))
    sign = cmac.hexdigest()

    return sign


def get_header():

    headers = {'x-api-key': api_key}
    return headers;