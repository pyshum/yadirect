import json
import requests
from datetime import date, timedelta

from django.conf import settings


yesterday = date.today() - timedelta(days=1)
dby = yesterday - timedelta(days=1)
yesterday.strftime('%y-%m-%d')

payload = {
        "jsonrpc": " 2.0",
        "id": settings.COMAGIC_ID,
        "method": "get.calls_report",
        "params": {
            "access_token": settings.COMAGIC_TOKEN,
            "offset": 0,
            "limit": 10000,
            'date_from': dby.strftime('%y-%m-%d'),
            'date_till': yesterday.strftime('%y-%m-%d'),
            filter: {
                'field': settings.COMAGIC_DOMAIN_NAME,
                'operator': "=",
                'value': settings.COMAGIC_SITE_NAME
            },
            'fields': [
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

url = 'https://callapi.comagic.ru/v4.0'
r = requests.post(url, data=json.dumps(payload))
sites = json.loads(r.text)
print(sites)

