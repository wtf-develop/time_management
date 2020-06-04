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
        'not_found': 'Not found',
        'logout': 'LogOut',
        'search': 'Search',
        'video_link': 'https://youtu.be/J_iGJ9E2TtU',
        'information': 'Information',
        'settings': 'Settings',

        'device_sync': 'Your devices',
        'common_tasks': 'Common tasks',
        'list_global_plan': 'Plan for the week',
        'list_calendar': 'Calendar view',
        'list_notes': 'Notes list',

    },
    'ru': {
        "application": 'Запоминатор',
        'login': 'Имя пользователя',
        'password': 'Пароль',
        'remember': 'Запомнить',
        'submit_login': 'Вход',
        'error': 'Ошибка',
        'bad_request': 'Неверный запрос',
        'not_found': 'Не найдено',
        'logout': 'Выход',
        'search': 'Поиск',
        'video_link': 'https://youtu.be/cv3NzFa1VyU',
        'information': 'Информация',
        'settings': 'Настройки',

        'device_sync': 'Ваши устройства',
        'common_tasks': 'Общие задачи',
        'list_global_plan': 'План на неделю',
        'list_calendar': 'Просмотр календаря',
        'list_notes': 'Список заметок',

    },
    'de': {
        "application": 'MachEs!',
        'login': 'Benutzer',
        'password': 'Passwort',
        'remember': 'Erinnere mich',
        'submit_login': 'Anmelden',
        'error': 'Fehler',
        'bad_request': 'Ungültige Anforderung',
        'not_found': 'Nicht gefunden',
        'logout': 'Ausloggen',
        'search': 'Suche',
        'information': 'Information',
        'settings': 'Einstellungen'


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
