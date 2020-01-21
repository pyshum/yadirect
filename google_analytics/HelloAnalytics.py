"""A simple example of how to access the Google Analytics API."""

from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def get_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = ServiceAccountCredentials.from_p12_keyfile(
        filename='/home/m108/api-project-439269810364-f71647adb3a0.p12',
        service_account_email='439269810364@developer.gserviceaccount.com',
        scopes=scopes
    )

    # Build the service object.
    service = build(api_name, api_version, credentials=credentials)

    return service


def get_first_profile_id(service):
    # Use the Analytics service object to get the first profile id.

    # Get a list of all Google Analytics accounts for this user
    accounts = service.management().accounts().list().execute()

    if accounts.get('items'):
        # Get the first Google Analytics account.
        # print(accounts.get('items'))
        account = accounts.get('items')[0].get('id')

        # Get a list of all the properties for the first account.
        properties = service.management().webproperties().list(
                accountId=account).execute()

        if properties.get('items'):
            # Get the first property id.
            property = properties.get('items')[0].get('id')

            # Get a list of all views (profiles) for the first property.
            profiles = service.management().profiles().list(
                    accountId=account,
                    webPropertyId=property).execute()

            if profiles.get('items'):
                # return the first view (profile) id.
                return profiles.get('items')[0].get('id')

    return None


def get_results(service, profile_id):
    # Use the Analytics Service Object to query the Core Reporting API
    # for the number of sessions within the past seven days.
    return service.data().ga().get(
            ids='ga:' + profile_id,
            start_date='7daysAgo',
            end_date='today',
            metrics='ga:sessions'
    ).execute()


def print_results(results):
    # Print data nicely for the user.
    if results:
        print('View (Profile):', results.get('profileInfo').get('profileName'))
        print('Total Sessions:', results.get('rows')[0][0])

    else:
        print('No results found')


def main():
    # Define the auth scopes to request.
    scope = 'https://www.googleapis.com/auth/analytics.readonly'
    key_file_location = '/home/m108/api-project-439269810364-f71647adb3a0.p12'

    # Authenticate and construct service.
    service = get_service(
            api_name='analyticsreporting',
            api_version='v4',
            scopes=[scope, ],
            key_file_location=key_file_location)

    profile_id = get_first_profile_id(service)
    print_results(get_results(service, profile_id))


if __name__ == '__main__':
    main()
