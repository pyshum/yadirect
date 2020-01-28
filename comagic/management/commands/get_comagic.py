import json
import requests
from datetime import datetime, date, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone

from comagic.models import APIData

# from yadirect_api.models import ApiData

from google_analytics.hello_analytics_v4 import export_response


class Command(BaseCommand):

    help = 'Команда получает данные с API Яндекс.Директ.'

    def handle(self, *args, **options):

        try:
            # Вычисляем начало текущей недели - week_start. В понедельник началом считается прошлый понедельник.
            current_weekday = date.today().weekday()
            week_start = date.today() - timedelta(
                days=(current_weekday + 7 if current_weekday == 0 else current_weekday)
            )

            payload = {
                "jsonrpc": "2.0",
                "id": settings.COMAGIC_ID,
                "method": "get.calls_report",
                "params": {
                    "access_token": settings.COMAGIC_TOKEN,
                    "offset": 0,
                    "limit": settings.COMAGIC_LIMIT,
                    "date_from": week_start.strftime('%Y-%m-%d 00:00:00'),
                    "date_till": date.today().strftime('%Y-%m-%d 00:00:00'),
                    "filter": {
                        "field": settings.COMAGIC_DOMAIN_NAME,
                        "operator": "=",
                        "value": settings.COMAGIC_SITE_NAME
                    },
                    "fields": [
                        "start_time",
                        "contact_phone_number",
                        "communication_type",
                        "tags",
                        "campaign_name",
                        "utm_source",
                        "utm_medium",
                        "utm_term",
                        "utm_content",
                        "utm_campaign"
                    ]

                }
            }

            url = 'https://dataapi.comagic.ru/v2.0'
            r = requests.post(url, data=json.dumps(payload))
            sites = json.loads(r.text)

            if sites:
                cnt_created = 0
                cnt_updated = 0

                for d in sites.get('result', {}).get('data', []):
                    filter_dict = {
                        'date': timezone.get_current_timezone().localize(
                            datetime.strptime(d.get('start_time'), '%Y-%m-%d %H:%M:%S')
                        ),
                        'callerNumber': d.get('contact_phone_number')
                    }
                    data_obj = APIData.objects.filter(
                        date__gte=week_start - timedelta(days=7),  # Выбираем в базе даты за текущую + прошедшую неделю
                        **filter_dict
                    )

                    data_dict = {
                        'callTags': f'{d.get("tags")}',
                        'source': d.get('utm_source'),
                        'source_type': d.get('tags', [])[0].get('tag_name'),
                        'utmCampaign': d.get('utm_campaign'),
                        'utmContent': d.get('utm_content'),
                        'utmMedium': d.get('utm_medium'),
                        'utmSource': d.get('utm_source'),
                        'utmTerm': d.get('utm_term'),
                        'location': '',
                        'communication_type': '',
                    }

                    if len(data_obj) != 0:
                        obj = data_obj.first()
                        data_dict.update({
                            'updated_at': timezone.get_current_timezone().localize(
                                datetime.now()
                            )
                        })
                        # print('data obj', obj.date, obj.callerNumber)
                        APIData.objects.filter(id=obj.id).update(**data_dict)
                        cnt_updated += 1

                        if cnt_updated % 10 == 0:
                            print('so far updated: ', cnt_updated)

                    else:
                        data_dict.update(filter_dict)
                        APIData.objects.create(**data_dict)
                        cnt_created += 1

                        if cnt_created % 10 == 0:
                            print('so far created: ', cnt_created)

                print(f'Created: {cnt_created};\n Updated: {cnt_updated};\n Total: {cnt_updated + cnt_created}')

        except Exception as e:
            print(e)
