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
        'wait_1_min': 'Please wait 60 seconds until your next login attempt',
        'user_not_found': 'User was not found or password is incorrect',
        'warning': 'Warning',
        'attention': 'Attention',
        'no_tasks_week': 'No tasks available for the next 7 days',
        'sunday': 'Sunday',
        'monday': 'Monday',
        'tuesday': 'Tuesday',
        'wednesday': 'Wednesday',
        'thursday': 'Thursday',
        'friday': 'Friday',
        'saturday': 'Saturday',
        'after_tomorrow': 'After tomorrow',
        'jan': 'January',
        'feb': 'February',
        'mar': 'March',
        'apr': 'April',
        'may': 'May',
        'jun': 'June',
        'jul': 'July',
        'aug': 'August',
        'sep': 'September',
        'oct': 'October',
        'nov': 'November',
        'dec': 'December',
        'timer_event': 'Timer',
        'date_event': 'Date',
        'no_calendar_events': 'No events available',
        'no_notes': 'There is no notes was created yet',
        'registration_success': 'Registration complete!\nPlease do not change your Login without Deregistration.\nNow you can use your Login and Password for Web',
        'sync_success': 'Sync is completed',
        'confirm_invite': 'Invite was approved. This device can send tasks to you',
        'device_link_removed': 'Device was removed from your access area',
        'sharing_complete': 'Selected tasks now available on this devices',
        'timers': 'Timers',
        'dates': 'Dates',
        'notes': 'Notes',
        'geo': 'Locations',
        'links': 'Sharing',
        'remove': 'Remove',
        'permission_denied': 'Permission denied',

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
        'remove_account_message': 'Все стерто, но это... возвращайся, если что',
        'wait_1_min': 'Подождите 60 секунд до следующей попытки входа',
        'user_not_found': 'Пользователь с таким именем не найден или пароль введен неправильно',
        'warning': 'Предупреждение',
        'attention': 'Внимание',
        'no_tasks_week': 'На следующие 7 дней задач нет никаких',
        'sunday': 'Воскресение',
        'monday': 'Понедельник',
        'tuesday': 'Вторник',
        'wednesday': 'Среда',
        'thursday': 'Четверг',
        'friday': 'Пятница',
        'saturday': 'Суббота',
        'after_tomorrow': 'Послезавтра',
        'jan': 'Января',
        'feb': 'Февраля',
        'mar': 'Марта',
        'apr': 'Апреля',
        'may': 'Мая',
        'jun': 'Июня',
        'jul': 'Июля',
        'aug': 'Августа',
        'sep': 'Сентября',
        'oct': 'Октября',
        'nov': 'Ноября',
        'dec': 'Декабря',
        'timer_event': 'Таймер',
        'date_event': 'Дата',
        'no_calendar_events': 'Событий никаких нет',
        'no_notes': 'Пока что нет ни одной заметки',
        'registration_success': 'Регистрация подтверждена!\nПожалуйста не меняйте имя пользователя без отмены текущей регистрации. Я предупредил!\nИмя пользователя и пароль теперь можно использовать для входа на портал синхронизации',
        'sync_success': 'Данные синхронизированы',
        'confirm_invite': 'Приглашение подтверждено. Это устройство теперь может присылать вам задачи.',
        'device_link_removed': 'Устройство было удалено из вашей области видимости',
        'sharing_complete': 'Выбранные задачи теперь доступны для этих устройств',
        'timers': 'Таймеры',
        'dates': 'Даты',
        'notes': 'Заметки',
        'geo': 'Локации',
        'links': 'Пересылка',
        'remove': 'Удалить',
        'permission_denied': 'Доступ запрещен',

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
