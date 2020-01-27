import json
import requests
from datetime import datetime, date, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand

from comagic.models import APIData

# from yadirect_api.models import ApiData

from google_analytics.hello_analytics_v4 import export_response


class Command(BaseCommand):

    help = 'Команда получает данные с API Яндекс.Директ.'

    def handle(self, *args, **options):

        try:
            current_weekday = date.today().weekday()
            week_start = date.today() - timedelta(
                days=(current_weekday+7 if current_weekday == 0 else current_weekday)
            )
            # else:
            #     week_start = date.today() - timedelta(days=datetime.today().weekday())
            yesterday = date.today() - timedelta(days=14)
            dby = yesterday - timedelta(days=1)

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
                cnt_total = 0

                for d in sites.get('result', {}).get('data', []):
                    data_obj, created = APIData.objects.get_or_create(
                        date=d.get('start_time'),
                        callerNumber=d.get('contact_phone_number')
                    )
                    if created:
                        cnt_created += 1
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

                    for k, v in data_dict.items():
                        setattr(data_obj, k, v)
                        data_obj.save()
                        cnt_total += 1

                print(f'Created: {cnt_created};\n Updated: {cnt_total - cnt_created};\n Total: {cnt_total}')

        except Exception as e:
            print(e)
