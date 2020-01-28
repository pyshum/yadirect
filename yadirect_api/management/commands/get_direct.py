from django.conf import settings
from django.core.management.base import BaseCommand

# from yadirect_api.models import ApiData
from yadirect_api.models import APIData

from yadirect_api.yadirect import response_data


class Command(BaseCommand):

    help = 'Команда получает данные с API Яндекс.Директ.'

    def handle(self, *args, **options):

        try:
            data_str = response_data(settings.TOKEN)
            data = data_str.split('\n')[:-1]
            total_rows = data[-1].split(':')
            values = [l.split('\t') for l in data[2:-1]]
            print('values: ', values)
            for value in values:
                api_data = APIData.objects.create(
                    # tagline={
                    #     'type': data[0].strip('"'),
                    #     'header': data[1].split('\t'),
                    #     'rows': [l.split('\t') for l in data[2:-1]],
                    #     total_rows[0]: total_rows[1].strip()
                    # },
                    Date=value[0],
                    CampaignId=value[1],
                    Clicks=value[2],
                    Cost=value[3]
                )
        #     def to_representation(self, obj):
        #         result = {}
        #         row = obj.data.get('rows')
        #         header = obj.data.get('header')
        #         if row and len(row) != 0:
        #             result = dict(zip(header, row[0]))
        #         return result

        except Exception as e:
            print(e)
