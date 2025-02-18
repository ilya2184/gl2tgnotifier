import re

def clean_subject(title):
    # Удаляем все символы, кроме русских букв, цифр и знаков препинания
    cleaned_title = re.sub(r'[^А-Яа-яЁё0-9\s,.!?;:()-]', '', title)
    
    # Удаляем пробелы в начале и конце строки
    cleaned_title = cleaned_title.strip()
    
    # Заменяем двойные пробелы на одинарные
    cleaned_title = re.sub(r'\s+', ' ', cleaned_title)
    
    return cleaned_title

def prepare_description(description):
    # Заменяем ссылки на изображения на текст "(изображение)"
    cleaned_description = re.sub(r'!\[image\]\(.*?\)\{.*?\}', '(изображение)', description)
    return cleaned_description

def prepare_message(action, data):
    object_attributes = data['object_attributes']
    assignee = data.get('assignee', {})

    action_text = ""
    subject = clean_subject(object_attributes['title'])
    description = prepare_description(object_attributes['description'])
    assignee_name = assignee.get('name', 'Не назначена')
    separator = "----------"  # Разделитель

    if action == "open":
        action_text = f"Открыта задача #{object_attributes['id']}."
        text = f"{description}\n{separator}\nОтветственный: {assignee_name}"
    elif action == "close":
        action_text = f"Закрыта задача #{object_attributes['id']}."
        text = f"{description}\n{separator}\nОтветственный: {assignee_name}"
    elif action == "reopen":
        action_text = f"Повторно открыта задача #{object_attributes['id']}."
        text = f"{description}\n{separator}\nОтветственный: {assignee_name}"
    elif action == "update":
        action_text = f"Обновлена задача #{object_attributes['id']}."
        text = f"{description}\n{separator}\nОтветственный: {assignee_name}"
    else:
        return {"subject": "Ошибка", "text": "Неизвестное действие с задачей"}

    return {
        "action": action_text,
        "subject": subject,
        "text": text
    }