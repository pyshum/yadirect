import json
import requests
from datetime import datetime, date, timedelta

from calltouch.calltouch_definition import CalltouchApi
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from calltouch.models import APIData

# from yadirect_api.models import ApiData

from google_analytics.hello_analytics_v4 import export_response


class Command(BaseCommand):

    help = 'Команда получает данные с CallTouch.'

    def handle(self, *args, **options):

        try:
            # Вычисляем начало текущей недели - week_start. В понедельник началом считается прошлый понедельник.
            current_weekday = date.today().weekday()
            week_start = date.today() - timedelta(
                days=(current_weekday + 14 if current_weekday == 0 else current_weekday + 7)
            )

            pages = []
            config = {
                'siteId': settings.CALLTOUCH_SITE_ID,
                'token': settings.CALLTOUCH_CLIENT_API_ID
            }
            date_from = week_start.strftime('%d/%m/%Y')
            date_to = date.today().strftime('%d/%m/%Y')

            ct = CalltouchApi(config.get('siteId'), config.get('token'))
            stats = ct.captureStats(date_from, date_to, type='callsByDate')
            """Помимо такого использования, можно явно указать степень разбиения статистики.
            Например:
            stats = ct.captureStats('11/07/2017', '11/07/2017', 'callsTotal')
            """
            pages.append(stats)
            if stats.get('pageTotal') > 1:
                for i in list(range(stats.get('pageTotal'), stats.get('pageTotal') + 1)):
                    pages.append(ct.captureStats(date_from, date_to, type='callsByDate', page=i))

            # return pages

            if pages:
                cnt_created = 0
                cnt_updated = 0

                for page in pages:

                    for record in page.get('records', []):
                        filter_dict = {
                            'date': timezone.get_current_timezone().localize(
                                datetime.strptime(record.get('date'), '%d/%m/%Y %H:%M:%S')
                            ),
                            'callerNumber': record.get('callerNumber')
                        }
                        try:
                            # Выбираем в базе даты за текущую + прошедшую неделю
                            data_obj = APIData.objects.filter(
                                date__gte=week_start - timedelta(days=7),
                                **filter_dict
                            ) or []
                        except Exception as e:
                            data_obj = []
                            print(e)

                        data_dict = {
                            'callerNumber': record.get('callerNumber'),
                            'callTags': sum([ct.get('names', '') for ct in record.get('callTags', [])], []),
                            'source': record.get('source'),
                            'utmSource': record.get('utmSource'),
                            'utmMedium': record.get('utmMedium'),
                            'utmCampaign': record.get('utmCampaign'),
                            'utmContent': record.get('utmContent'),
                            'utmTerm': record.get('utmTerm'),
                            'uniqueCall': record.get('uniqueCall'),
                        }

                        if len(data_obj) != 0:
                            obj = data_obj.first()
                            data_dict.update({
                                'updated_at': timezone.get_current_timezone().localize(
                                    datetime.now()
                                )
                            })
                            # print('data dict:', data_dict)
                            APIData.objects.filter(id=obj.id).update(**data_dict)
                            cnt_updated += 1

                            if cnt_updated % 10 == 0:
                                print('so far updated: ', cnt_updated)

                        else:
                            data_dict.update(filter_dict)
                            # print('data dict updated: ', data_dict)
                            APIData.objects.create(**data_dict)
                            cnt_created += 1

                            if cnt_created % 10 == 0:
                                print('so far created: ', cnt_created)

                print(f'Created: {cnt_created};\n Updated: {cnt_updated};\n Total: {cnt_updated + cnt_created}')

        except Exception as e:
            print('error: ', e)

