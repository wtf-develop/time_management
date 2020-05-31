import json

lang = {
    'en': {
        "application": 'Reminder',
        'login': 'User',
        'password': 'Password',
        'remember': 'Remember me',
        'submit_login': 'LogIn'

    },
    'ru': {
        "application": 'Запоминатор',
        'login': 'Имя пользователя',
        'password': 'Пароль',
        'remember': 'Запомнить',
        'submit_login': 'Вход'

    },
    'de': {
        "application": 'MachEs!',
        'login': 'Benutzer',
        'password': 'Passwort',
        'remember': 'Erinnere mich',
        'submit_login': 'Anmelden'

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
