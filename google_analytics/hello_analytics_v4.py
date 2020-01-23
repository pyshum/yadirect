"""Hello Analytics Reporting API V4."""

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from pathlib import Path

from .models import APIData

scopes = ['https://www.googleapis.com/auth/analytics.readonly', ]
filename = f'{str(Path.home())}/api-project-439269810364-f71647adb3a0.p12'
VIEW_ID = '184110713'


def initialize_analyticsreporting():
    """Initializes an Analytics Reporting API V4 service object.

    Returns:
    An authorized Analytics Reporting API V4 service object.
    """
    credentials = ServiceAccountCredentials.from_p12_keyfile(
        filename=filename,
        scopes=scopes,
        service_account_email='439269810364@developer.gserviceaccount.com'
    )

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics


def save_report(response):
    db_list = []
    # header_dimensions = response.get('reports')[0].get('columnHeader').get('dimensions', [])
    # header_metrics = [mh.get('name') for mh in
    #                   response.get(
    #                       'reports'
    #                   )[0].get(
    #                       'columnHeader'
    #                   ).get('metricHeader', {}).get('metricHeaderEntries', [])]

    for report in response.get('reports', []):
        column_header = report.get('column_header', {})
        dimension_headers = column_header.get('dimensions', [])
        metric_headers = column_header.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            date_range_values = row.get('metrics', [])
            db_dict = {}

            # for header, dimension in zip(dimension_headers, dimensions):
            #     print(header + ': ' + dimension)
            db_dict.update(dict(zip(dimension_headers, dimensions)))

            # for i, values in enumerate(date_range_values):
            #     print('Date range: ' + str(i))
            #     for metricHeader, value in zip(metric_headers, values.get('values')):
            #         print(metricHeader.get('name') + ': ' + value)
            db_dict.update(dict(zip([mh.get('name') for mh in metric_headers], date_range_values[0].get('values'))))

            api_data = APIData.objects.create(
                campaign=db_dict.get('ga:campaign'),
                date=db_dict.get('ga:date'),
                medium=db_dict.get('ga:medium'),
                source=db_dict.get('ga:source'),
                sessions=db_dict.get('ga:sessions'),
                pageviews=db_dict.get('ga:pageviews'),
                adClicks=db_dict.get('ga:adClicks'),
                adCost=db_dict.get('ga:adCost'),
                impressions=db_dict.get('ga:impressions')
            )

            db_list.append(db_dict)

    return db_list


def get_report(analytics):
    """Queries the Analytics Reporting API V4.

    Args:
    analytics: An authorized Analytics Reporting API V4 service object.
    Returns:
    The Analytics Reporting API V4 response.
    ga:date,ga:campaign,ga:medium,ga:source,ga:adClicks,ga:adCost,ga:impressions,ga:pageviews,ga:sessions
    """
    report = analytics.reports().batchGet(
        body={
            'reportRequests': [
                {
                    'viewId': VIEW_ID,
                    'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
                    'metrics': [
                        {'expression': 'ga:sessions'},
                        {'expression': 'ga:pageviews'},
                        {'expression': 'ga:adClicks'},
                        {'expression': 'ga:adCost'},
                        {'expression': 'ga:impressions'}
                    ],
                    'dimensions': [
                        # {'name': 'ga:country'},
                        {'name': 'ga:campaign'},
                        {'name': 'ga:date'},
                        {'name': 'ga:medium'},
                        {'name': 'ga:source'},
                    ]
                }
            ]
        }
    ).execute()
    # print(report)
    return report


def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
    response: An Analytics Reporting API V4 response.
    """
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                print(header + ': ' + dimension)

            for i, values in enumerate(dateRangeValues):
                print('Date range: ' + str(i))
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    print(metricHeader.get('name') + ': ' + value)


def export_response():
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    return response


def main():
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    save_report(response)
    # print_response(response)


if __name__ == '__main__':
    main()
