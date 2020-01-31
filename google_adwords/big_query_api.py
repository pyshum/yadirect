from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('bi-test-1-217811-1d17b72ec13d.json')

project_id = 'bi-test-1-217811'

client = bigquery.Client(credentials=credentials, project=project_id)
