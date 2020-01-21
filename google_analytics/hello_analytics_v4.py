"""Hello Analytics Reporting API V4."""

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

scopes = ['https://www.googleapis.com/auth/analytics.readonly', ]
filename = '/home/m108/api-project-439269810364-f71647adb3a0.p12'
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
    #                   response.get('reports')[0].get('columnHeader').get('metricHeader', {}).get('metricHeaderEntries', [])]

    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                print(header + ': ' + dimension)
            db_list.append(dict(zip(dimensionHeaders, dimensions)))

            for i, values in enumerate(dateRangeValues):
                print('Date range: ' + str(i))
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    print(metricHeader.get('name') + ': ' + value)
            db_list[-1].update(dict(zip(dimensionHeaders, dimensions)))


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


def main():
    analytics = initialize_analyticsreporting()
    response = get_report(analytics)
    # print_response(response)


if __name__ == '__main__':
    main()
