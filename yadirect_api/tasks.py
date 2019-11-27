from datetime import timedelta

from celery.task import periodic_task

from yadirect_api.models import ApiData


@periodic_task(run_every=timedelta(min(3)))
def save_data(response_data_func, token):
    pass

    # try:
    #     data = response_data_func(token)
    #     total_rows = data[-1].split(':')
    #     api_data = ApiData.objects.create(
    #         data={
    #             'type': data[0],
    #             'header': data[1].split('\t'),
    #             'rows': data[2:-1],
    #             total_rows[0]: total_rows[1].strip()
    #         }
    #     )
    #
    # except Exception as e:
    #     print(e)
