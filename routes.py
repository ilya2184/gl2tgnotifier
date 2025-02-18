
from flask import request, jsonify, abort
import json
import messagegen
import messagesender

config = None  # Глобальная переменная для хранения конфигурации

def load_config():
    global config
    with open('config/config.json') as config_file:
        config = json.load(config_file)

def setup_routes(app):

    load_config()  # Загружаем конфигурацию при старте приложения

    @app.route('/ping', methods=['GET'])
    def ping():
        return jsonify({"Ready": ""})

    @app.route('/webhook/issues', methods=['POST'])
    def issues():
        # Проверка заголовка X-Gitlab-Webhook-UUID
        webhook_uuid = request.headers.get('X-Gitlab-Webhook-UUID')
        if webhook_uuid not in config['webhook_uuids']:
            return abort(401, webhook_uuid)  # Неавторизован

        # Проверка заголовка X-Gitlab-Event
        gitlab_event = request.headers.get('X-Gitlab-Event')
        if gitlab_event != 'Issue Hook':
            return abort(400)  # Плохой запрос

        # Обработка тела запроса
        data = request.get_json()
        if not data or 'object_attributes' not in data:
            return abort(400)  # Плохой запрос

        action = data['object_attributes'].get('action')
        if action not in ['open', 'close', 'reopen', 'update']:
            return abort(400)  # Плохой запрос
        
        # Подготовка сообщения
        message = messagegen.prepare_message(action, data)

        # Отправка сообщения
        messagesender.send_message(message, config, webhook_uuid)

        return jsonify({"message": "Hook successful."})

