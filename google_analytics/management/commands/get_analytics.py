from django.conf import settings
from django.core.management.base import BaseCommand

# from yadirect_api.models import ApiData
from google_analytics.models import APIData

from google_analytics.hello_analytics_v4 import export_response


class Command(BaseCommand):

    help = 'Команда получает данные с API Яндекс.Директ.'

    def handle(self, *args, **options):

        try:
            response = export_response()

            for report in response.get('reports', []):
                column_header = report.get('columnHeader', {})
                dimension_headers = column_header.get('dimensions', [])
                metric_headers = column_header.get('metricHeader', {}).get('metricHeaderEntries', [])

                for row in report.get('data', {}).get('rows', []):

                    dimensions = row.get('dimensions', [])
                    date_range_values = row.get('metrics', [])
                    db_dict = {}

                    db_dict.update(dict(zip(dimension_headers, dimensions)))

                    db_dict.update(dict(zip([mh.get('name') for mh in metric_headers], date_range_values[0].get('values'))))
                    data_str = db_dict.get('ga:date')

                    api_data = APIData.objects.create(
                        campaign=db_dict.get('ga:campaign'),
                        date=f'{data_str[0:4]}-{data_str[4:6]}-{data_str[6:8]}',
                        medium=db_dict.get('ga:medium'),
                        source=db_dict.get('ga:source'),
                        sessions=db_dict.get('ga:sessions'),
                        pageviews=db_dict.get('ga:pageviews'),
                        adClicks=db_dict.get('ga:adClicks'),
                        adCost=db_dict.get('ga:adCost'),
                        impressions=db_dict.get('ga:impressions')
                    )

        except Exception as e:
            print(e)
