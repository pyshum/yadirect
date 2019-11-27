from django.conf import settings
from django.core.management.base import BaseCommand

from yadirect_api.models import ApiData
from yadirect_api.yadirect import response_data


class Command(BaseCommand):

    help = 'Команда получает данные с API Яндекс.Директ.'

    def handle(self, *args, **options):

        try:
            data_str = response_data(settings.TOKEN)
            data = data_str.split('\n')[:-1]
            total_rows = data[-1].split(':')
            api_data = ApiData.objects.create(
                data={
                    'type': data[0].strip('"'),
                    'header': data[1].split('\t'),
                    'rows': [l.split('\t') for l in data[2:-1]],
                    total_rows[0]: total_rows[1].strip()
                }
            )

        except Exception as e:
            print(e)
