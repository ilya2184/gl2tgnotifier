
from requests import post
from flask import abort
import smtplib
from email.mime.text import MIMEText

def send_message(message, config, webhook_uuid):
    send_type = config['webhook_tokens'][webhook_uuid]['type']

    if send_type == 'telegram':
        return send_telegram(message, config, webhook_uuid)
    elif send_type == 'email':
        return send_email(message, config, webhook_uuid)
    elif send_type == 'bitrix':
        return send_bitrix(message, config, webhook_uuid)
    else:
        return abort(400, "Invalid input")  # Неверный тип отправки

def send_telegram(message, config, webhook_uuid):
    # Получение токена и группы из конфигурации
    token = config['webhook_tokens'][webhook_uuid]['token']
    group = config['webhook_tokens'][webhook_uuid]['group']

    # Логика отправки сообщения в Telegram
    text_message = (f"{message['action']}"
        + f"\n{message['subject']}"
        + f"\n{message['text']}")
    response = post(f"https://api.telegram.org/bot{token}/sendMessage", 
                    data={"chat_id": group, "text": text_message})
    return response.json()

def send_email(message, config, webhook_uuid):
    # Получение данных для отправки email из конфигурации
    email_config = config['webhook_tokens'][webhook_uuid]
    recipient = email_config['recipient']
    subject = message['subject']  # Используем subject из структуры message
    smtp_server = email_config['smtp_server']
    smtp_port = email_config['smtp_port']
    username = email_config['username']
    password = email_config['password']

    # Логика отправки email
    msg = MIMEText(message['text'])  # Используем text из структуры message
    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = recipient

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Защита с помощью TLS
            server.login(username, password)
            server.sendmail(username, recipient, msg.as_string())
        return {"status": "success", "message": "Email sent successfully"}
    except Exception as e:
        return abort(500, f"Email sending failed: {str(e)}")

def send_bitrix(message, config, webhook_uuid):
    # Логика отправки сообщения в Bitrix
    bitrix_webhook = config['webhook_tokens'][webhook_uuid]['bitrix_webhook']
    
    response = post(bitrix_webhook, json={"message": message['text']})  # Отправляем текст сообщения
    return response.json()
