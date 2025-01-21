import ssl
import http.client
import json
import tempfile
from django.conf import settings

def call_jsonrpc(method_name, params=None, request_id=1):
    """
    Отправляет JSON-RPC 2.0 запрос к эндпоинту settings.JSONRPC_ENDPOINT
    с двухсторонней TLS-аутентификацией.
    Возвращает dict-ответ (result или error).
    """
    if params is None:
        params = {}

    # Формируем тело запроса по спецификации JSON-RPC 2.0
    payload = {
        "jsonrpc": "2.0",
        "method": method_name,
        "params": params,
        "id": request_id
    }
    body = json.dumps(payload).encode('utf-8')

    # Подготовка SSL-контекста
    with tempfile.NamedTemporaryFile(delete=False) as cert_file, \
         tempfile.NamedTemporaryFile(delete=False) as key_file:
        cert_file.write(settings.CLIENT_CERT.encode('utf-8'))
        key_file.write(settings.CLIENT_KEY.encode('utf-8'))
        cert_file.flush()
        key_file.flush()
        
        ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        # Если нужно отключить проверку сертификата сервера (не рекомендуется в бою!):
        # ssl_context.check_hostname = False
        # ssl_context.verify_mode = ssl.CERT_NONE

        # Подключаем клиентские сертификат и ключ
        ssl_context.load_cert_chain(certfile=cert_file.name, keyfile=key_file.name)

        # Пример: эндпоинт = "https://slb.medv.ru/api/v2/"
        # Разделим URL на хост и путь
        host = "slb.medv.ru"
        url_path = "/api/v2/"  # <-- от / и дальше

        conn = http.client.HTTPSConnection(host, context=ssl_context)
        try:
            conn.request("POST", url_path, body=body, headers={
                "Content-Type": "application/json"
            })
            response = conn.getresponse()
            response_data = response.read().decode('utf-8')
        finally:
            conn.close()

    # Парсим ответ
    try:
        json_response = json.loads(response_data)
    except ValueError:
        # Если неожиданно вернулась не-JSON строка
        return {
            "error": {
                "code": -32700,
                "message": f"Parse error: could not decode JSON. Raw response: {response_data}"
            }
        }

    return json_response
