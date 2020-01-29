import pprint
import json
import datetime

import json
import requests
from datetime import datetime, date, timedelta

from calltouch.calltouch_definition import CalltouchApi
from django.conf import settings
from django.core.management.base import BaseCommand

from .calltouch_definition import CalltouchApi


def get_calltouch():

    try:
        config = {'name': '', 'siteId': settings.CALLTOUCH_SITE_ID, 'token': settings.CALLTOUCH_CLIENT_API_ID}

        ct = CalltouchApi(config.get('siteId'), config.get('token'))
        stats = ct.captureStats('10/01/2020', '29/01/2020', type='callsByDate')
        """Помимо такого использования, можно явно указать степень разбиения статистики.
        Например:
        stats = ct.captureStats('11/07/2017', '11/07/2017', 'callsTotal')
        """
        print(stats.get('page'))
        print(stats.get('pageTotal'))

    except Exception as e:
        print(e)

    return stats
