import os
import time
import hashlib
import hmac
import base64

def make_sign(token: str,secret: str):
    nonce = ''
    t = int(round(time.time() * 1000))
    string_to_sign = bytes(f'{token}{t}{nonce}', 'utf-8')
    secret = bytes(secret, 'utf-8')
    sign = base64.b64encode(hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest())
    return sign, str(t), nonce

def make_request_header(token: str,secret: str) -> dict:
    sign,t,nonce = make_sign(token, secret)
    headers={
            "Authorization": token,
            "sign": sign,
            "t": str(t),
            "nonce": nonce
        }
    return headers

import requests
import json

base_url = 'https://api.switch-bot.com'

def get_device_list(deviceListJson='deviceList.json'):
    # tokenとsecretを貼り付ける
    token = "abd1abab99f85267fc351e0b05e96ffe60beee153d1fed36e03302112e1e5204d5c6c72bb31c23a400cee1381f7a72a5"
    secret = "0b41627b187cefb7badb96968624cfd8"

    devices_url = base_url + "/v1.1/devices/"

    headers = make_request_header(token, secret)

    try:
        # APIでデバイスの取得を試みる
        res = requests.get(devices_url, headers=headers)
        res.raise_for_status()

        print(res.text)
        deviceList = json.loads(res.text)
        # 取得データをjsonファイルに書き込み
        with open(deviceListJson, mode='wt', encoding='utf-8') as f:
            json.dump(deviceList, f, ensure_ascii=False, indent=2)

    except requests.exceptions.RequestException as e:
        print('response error:',e)


def lock(deviceId: str):
    # tokenとsecretを貼り付ける
    token = "abd1abab99f85267fc351e0b05e96ffe60beee153d1fed36e03302112e1e5204d5c6c72bb31c23a400cee1381f7a72a5"
    secret = "0b41627b187cefb7badb96968624cfd8"

    headers = make_request_header(token, secret)

    devices_url = base_url + "/v1.1/devices/" + deviceId + "/commands"
    data = {
        "commandType": "command",
        "command": "lock",
        "parameter": "default",
    }
    try:
        # ロック
        res = requests.post(devices_url, headers=headers, json=data)
        res.raise_for_status()
        print(res.text)

    except requests.exceptions.RequestException as e:
        print('response error:', e)


def unlock(deviceId: str):
    token = "abd1abab99f85267fc351e0b05e96ffe60beee153d1fed36e03302112e1e5204d5c6c72bb31c23a400cee1381f7a72a5"
    secret = "0b41627b187cefb7badb96968624cfd8"

    headers = make_request_header(token, secret)

    devices_url = base_url + "/v1.1/devices/" + deviceId + "/commands"
    data = {
        "commandType": "command",
        "command": "unlock",
        "parameter": "default",
    }
    try:
        # アンロック
        res = requests.post(devices_url, headers=headers, json=data)
        res.raise_for_status()
        print(res.text)

    except requests.exceptions.RequestException as e:
        print('response error:', e)
