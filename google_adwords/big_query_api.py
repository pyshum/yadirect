from gcloud.exceptions import NotFound
from google.cloud import bigquery
from google.oauth2 import service_account

credentials = service_account.Credentials.from_service_account_file('bi-test-1-217811-1d17b72ec13d.json')

project_id = 'bi-test-1-217811'

client = bigquery.Client(credentials=credentials, project=project_id)


def bq_create_dataset(dataset_id):
    # Create a dataset if not existing
    bigquery_client = client
    dataset_ref = bigquery_client.dataset(dataset_id)

    try:
        bigquery_client.get_dataset(dataset_ref)
        print(f'Dataset {dataset_id} existed.')
    except NotFound:
        dataset = bigquery.Dataset(dataset_ref)
        dataset = bigquery_client.create_dataset(dataset)
        print('Dataset {} created.'.format(dataset.dataset_id))


def bq_create_table(dataset_id, table_id, api_obj):
    # Create a table if not existing
    bigquery_client = bigquery.Client()
    dataset_ref = bigquery_client.dataset(dataset_id)

    # Prepares a reference to the table
    table_ref = dataset_ref.table(table_id)

    try:
        bigquery_client.get_table(table_ref)
    except NotFound:
        schema = get_table_schema(api_obj=api_obj)
        table = bigquery.Table(table_ref, schema=schema)
        table = bigquery_client.create_table(table)
        print('table {} created.'.format(table.table_id))


def get_table_schema(api_obj):

    objects_types = {
        'TextField': 'STRING',
        'DateTimeField': 'TIMESTAMP',
        'IntegerField': 'INTEGER'
    }

    BQ_TABLE_SCHEMA = []

    for onm in api_obj._meta.fields:
        BQ_TABLE_SCHEMA.append(
            bigquery.SchemaField(onm.name, objects_types.get(type(onm).__name__, 'STRING'), description=onm.name)
        )

    return BQ_TABLE_SCHEMA


def export_items_to_bigquery(dataset_id, table_id, api_model):
    # Instantiates a client
    bigquery_client = bigquery.Client()

    # Prepares a reference to the dataset
    dataset_ref = bigquery_client.dataset(dataset_id)

    table_ref = dataset_ref.table(table_id)
    table = bigquery_client.get_table(table_ref)  # API call

    rows_to_insert = []

    for obj in api_model.objects.all():
        rows_to_insert.append(
            [v for k, v in obj.__dict__.items()]
        )

    errors = bigquery_client.insert_rows(table, rows_to_insert)  # API request
    assert errors == []
