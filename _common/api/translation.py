import json

lang = {
    'en': {
        "application": 'Reminder',
        'login': 'User',
        'password': 'Password',
        'remember': 'Remember me',
        'submit_login': 'LogIn',
        'error': 'Error',
        'bad_request': 'Bad request',
        'not_found': 'Not found'

    },
    'ru': {
        "application": 'Запоминатор',
        'login': 'Имя пользователя',
        'password': 'Пароль',
        'remember': 'Запомнить',
        'submit_login': 'Вход',
        'error': 'Ошибка',
        'bad_request': 'Неверный запрос',
        'not_found': 'Не найдено'

    },
    'de': {
        "application": 'MachEs!',
        'login': 'Benutzer',
        'password': 'Passwort',
        'remember': 'Erinnere mich',
        'submit_login': 'Anmelden',
        'error': 'Fehler',
        'bad_request': 'Ungültige Anforderung',
        'not_found': 'Nicht gefunden'

    }

}


def get_array(lang_code):
    if lang is None:
        return json.dumps(lang['en'])
    if lang_code == 'en':
        return json.dumps(lang['en'])
    if (not (lang_code in lang)) or (lang[lang_code] is None):
        return json.dumps(lang['en'])
    result = lang['en']
    for key in lang[lang_code]:
        result[key] = lang[lang_code][key]
    return json.dumps(result)


def get_array_with_code(lang_code):
    if lang is None:
        return json.dumps({'code': 'en', 'data': lang['en']})
    if lang_code == 'en':
        return json.dumps({'code': 'en', 'data': lang['en']})
    if (not (lang_code in lang)) or (lang[lang_code] is None):
        return json.dumps({'code': 'en', 'data': lang['en']})
    result = lang['en']
    for key in lang[lang_code]:
        result[key] = lang[lang_code][key]
    return json.dumps({'code': lang_code, 'data': result})
