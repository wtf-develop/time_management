import json

from _common.api import auth

lang = {
    'en': {
        "application": 'PlanMe',
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
        'today': 'Today',
        'tomorrow': 'Tomorrow',

        'inreview': 'In Review',
        'approved': 'Approved',
        'inprogress': 'In Progress',
        'completed': 'Completed',
        'canceled': 'Canceled',
        'archived': 'Archived',
        'all_devices': 'All devices',
        'mobile_too_short': 'Minimum 4 symbols for each value',
        'remove_account_message': 'Ok, goodbye!',

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
        'today': 'Сегодня',
        'tomorrow': 'Завтра',

        'inreview': 'Черновые',
        'approved': 'Одобренные',
        'inprogress': 'В работе',
        'completed': 'Завершенные',
        'canceled': 'Отмененные',
        'archived': 'Архивные',
        'all_devices': 'Все устройства',
        'mobile_too_short': 'Минимум 4 символа для каждого поля',
        'remove_account_message': 'Прощай, но это... возвращайся, если что',

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
        'settings': 'Einstellungen',

        'device_sync': 'Ihre Geräte',
        'common_tasks': 'Gemeinsame Aufgaben',
        'list_global_plan': 'Plan für die Woche',
        'list_calendar': 'Kalenderansicht',
        'list_notes': 'Notizenliste',
        'today': 'Heute',
        'tomorrow': 'Morgen',

    }

}


def get_array(lang_code: str):  # for injecting into HTML pages
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


def get_array_with_code(lang_code: str):
    if lang_code is None:
        return ({'code': 'en', 'data': lang['en']})
    if lang_code == 'en':
        return ({'code': 'en', 'data': lang['en']})
    if (not (lang_code in lang)) or (lang[lang_code] is None):
        return ({'code': 'en', 'data': lang['en']})
    result = lang['en']
    for key in lang[lang_code]:
        result[key] = lang[lang_code][key]
    return ({'code': lang_code, 'data': result})


def getAppName(lang_code: str) -> str:
    return getValue('application', lang_code)


def getValue(key: str, lang_code: str = auth.req_language):
    if (lang_code is None) or (lang_code == 'en'):
        lang_code = 'en'
    if (not (lang_code in lang)) or (lang[lang_code] is None):
        lang_code = 'en'
    if key not in lang[lang_code]:
        lang_code = 'en'
    if (lang is None) or (lang_code not in lang) or (lang[lang_code] is None) or (key not in lang[lang_code]) or (
            lang[lang_code][key] is None):
        return key
    return lang[lang_code][key]
