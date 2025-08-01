# coding=utf-8

'''
requires Python 3.6 or later

pip install asyncio
pip install websockets

'''

import asyncio
import copy
import gzip
import json
import re
import ssl

import requests
import uuid_utils.compat as uuid
from typing import Dict

import websockets
from django.utils.translation import gettext as _

from common.utils.common import _remove_empty_lines
from models_provider.base_model_provider import MaxKBBaseModel
from models_provider.impl.base_tts import BaseTextToSpeech

MESSAGE_TYPES = {11: "audio-only server response", 12: "frontend server response", 15: "error message from server"}
MESSAGE_TYPE_SPECIFIC_FLAGS = {0: "no sequence number", 1: "sequence number > 0",
                               2: "last message from server (seq < 0)", 3: "sequence number < 0"}
MESSAGE_SERIALIZATION_METHODS = {0: "no serialization", 1: "JSON", 15: "custom type"}
MESSAGE_COMPRESSIONS = {0: "no compression", 1: "gzip", 15: "custom compression method"}

# version: b0001 (4 bits)
# header size: b0001 (4 bits)
# message type: b0001 (Full client request) (4bits)
# message type specific flags: b0000 (none) (4bits)
# message serialization method: b0001 (JSON) (4 bits)
# message compression: b0001 (gzip) (4bits)
# reserved data: 0x00 (1 byte)
default_header = bytearray(b'\x11\x10\x11\x00')

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


class VolcanicEngineTextToSpeech(MaxKBBaseModel, BaseTextToSpeech):
    volcanic_app_id: str
    volcanic_cluster: str
    volcanic_api_url: str
    volcanic_token: str
    params: dict

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.volcanic_api_url = kwargs.get('volcanic_api_url')
        self.volcanic_token = kwargs.get('volcanic_token')
        self.volcanic_app_id = kwargs.get('volcanic_app_id')
        self.volcanic_cluster = kwargs.get('volcanic_cluster')
        self.params = kwargs.get('params')

    @staticmethod
    def new_instance(model_type, model_name, model_credential: Dict[str, object], **model_kwargs):
        optional_params = {'params': {'voice_type': 'zh_female_cancan_mars_bigtts', 'speed_ratio': 1.0}}
        for key, value in model_kwargs.items():
            if key not in ['model_id', 'use_local', 'streaming']:
                optional_params['params'][key] = value
        return VolcanicEngineTextToSpeech(
            volcanic_api_url=model_credential.get('volcanic_api_url'),
            volcanic_token=model_credential.get('volcanic_token'),
            volcanic_app_id=model_credential.get('volcanic_app_id'),
            volcanic_cluster=model_credential.get('volcanic_cluster'),
            **optional_params
        )

    def check_auth(self):
        self.text_to_speech(_('Hello'))

    def text_to_speech(self, text):
        request_json = {
            "app": {
                "appid": self.volcanic_app_id,
                "token": "access_token",
                "cluster": self.volcanic_cluster
            },
            "user": {
                "uid": "uid"
            },
            "audio": {
                         "encoding": "mp3",
                         "volume_ratio": 1.0,
                         "pitch_ratio": 1.0,
                     } | self.params,
            "request": {
                "reqid": str(uuid.uuid7()),
                "text": '',
                "text_type": "plain",
                "operation": "xxx"
            }
        }
        text = _remove_empty_lines(text)

        return asyncio.run(self.submit(request_json, text))

    def is_cache_model(self):
        return False

    def token_auth(self):
        return {'Authorization': 'Bearer; {}'.format(self.volcanic_token)}

    async def submit(self, request_json, text):
        submit_request_json = copy.deepcopy(request_json)
        submit_request_json["request"]["operation"] = "submit"
        header = {"Authorization": f"Bearer; {self.volcanic_token}"}
        result = b''
        async with websockets.connect(self.volcanic_api_url, additional_headers=header, ping_interval=None,
                                      ssl=ssl_context) as ws:
            lines = [text[i:i + 200] for i in range(0, len(text), 200)]
            for line in lines:
                if self.is_table_format_chars_only(line):
                    continue
                submit_request_json["request"]["reqid"] = str(uuid.uuid7())
                submit_request_json["request"]["text"] = line
                payload_bytes = str.encode(json.dumps(submit_request_json))
                payload_bytes = gzip.compress(payload_bytes)  # if no compression, comment this line
                full_client_request = bytearray(default_header)
                full_client_request.extend((len(payload_bytes)).to_bytes(4, 'big'))  # payload size(4 bytes)
                full_client_request.extend(payload_bytes)  # payload
                await ws.send(full_client_request)
                result += await self.parse_response(ws)
        return result

    @staticmethod
    def is_table_format_chars_only(s):
        # 检查是否仅包含 "|", "-", 和空格字符
        return bool(s) and re.fullmatch(r'[|\-\s]+', s)

    @staticmethod
    async def parse_response(ws):
        result = b''
        while True:
            res = await ws.recv()
            protocol_version = res[0] >> 4
            header_size = res[0] & 0x0f
            message_type = res[1] >> 4
            message_type_specific_flags = res[1] & 0x0f
            serialization_method = res[2] >> 4
            message_compression = res[2] & 0x0f
            reserved = res[3]
            header_extensions = res[4:header_size * 4]
            payload = res[header_size * 4:]
            if header_size != 1:
                # print(f"           Header extensions: {header_extensions}")
                pass
            if message_type == 0xb:  # audio-only server response
                if message_type_specific_flags == 0:  # no sequence number as ACK
                    continue
                else:
                    sequence_number = int.from_bytes(payload[:4], "big", signed=True)
                    payload_size = int.from_bytes(payload[4:8], "big", signed=False)
                    payload = payload[8:]
                result += payload
                if sequence_number < 0:
                    break
                else:
                    continue
            elif message_type == 0xf:
                code = int.from_bytes(payload[:4], "big", signed=False)
                msg_size = int.from_bytes(payload[4:8], "big", signed=False)
                error_msg = payload[8:]
                if message_compression == 1:
                    error_msg = gzip.decompress(error_msg)
                error_msg = str(error_msg, "utf-8")
                raise Exception(f"Error code: {code}, message: {error_msg}")
            elif message_type == 0xc:
                msg_size = int.from_bytes(payload[:4], "big", signed=False)
                payload = payload[4:]
                if message_compression == 1:
                    payload = gzip.decompress(payload)
            else:
                break
        return result
