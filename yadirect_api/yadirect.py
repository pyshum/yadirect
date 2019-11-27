# -*- coding: utf-8 -*-
import requests
from requests.exceptions import ConnectionError
from time import sleep
import json

#  Method for correctly parsing UTF-8 encoded strings for both Python 3 and Python 2
import sys

if sys.version_info < (3,):
    def u(x):
        try:
            return x.encode("utf8")
        except UnicodeDecodeError:
            return x
else:
    def u(x):
        if type(x) == type(b''):
            return x.decode('utf8')
        else:
            return x

# --- Input data ---
#  Address of the Reports service for sending JSON requests (case-sensitive)
ReportsURL = 'https://api.direct.yandex.com/json/v5/campaigns'
# ReportsURL = 'https://api.direct.yandex.com/json/v5/reports'

# OAuth token of the user that requests will be made on behalf of
token = 'TOKEN'

# Login of the advertising agency client
# Required parameter if requests are made on behalf of an advertising agency
clientLogin = 'CLIENT_LOGIN'

# --- Preparing the request ---
#  Creating HTTP request headers
headers = {
           # OAuth token. The word Bearer must be used
           "Authorization": "Bearer " + token,
           # Login of the advertising agency client
           "Client-Login": clientLogin,
           # Language for response messages
           "Accept-Language": "en",
           # Mode for report generation
           "processingMode": "auto"
           # Format for monetary values in the report
           # "returnMoneyInMicros": "false",
           # Don't include the row with the report name and date range in the report
           # "skipReportHeader": "true",
           # Don't include the row with column names in the report
           # "skipColumnHeader": "true",
           # Don't include the row with the number of statistics rows in the report
           # "skipReportSummary": "true"
           }

# Creating the request message body
body = {
    "params": {
        "SelectionCriteria": {
        },
        "FieldNames": [
            "Date",
            "CampaignId",
            "Clicks",
            "Cost"
        ],
        "ReportName": "Report",
        "ReportType": "CAMPAIGN_PERFORMANCE_REPORT",
        "DateRangeType": "YESTERDAY",
        "Format": "TSV",
        "IncludeVAT": "YES",
        "IncludeDiscount": "YES"
    }
}

# Encoding the request message body as JSON
body = json.dumps(body, indent=4)

# --- Starting the request execution loop ---
# If HTTP code 200 is returned, output the report contents
# If HTTP code 201 or 202 is returned, send repeated requests
while True:
    try:
        req = requests.post(ReportsURL, body, headers=headers)
        req.encoding = 'utf-8'  # Mandatory response processing in UTF-8
        if req.status_code == 400:
            print("Invalid request parameters, or the report queue is full")
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            print("JSON code for the request: {}".format(u(body)))
            print("JSON code for the server response: \n{}".format(u(req.json())))
            break
        elif req.status_code == 200:
            print("Report created successfully")
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            print("Report contents: \n{}".format(u(req.text)))
            break
        elif req.status_code == 201:
            print("Report successfully added to the offline queue")
            retryIn = int(req.headers.get("retryIn", 60))
            print("Request will be resent in {} seonds".format(retryIn))
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            sleep(retryIn)
        elif req.status_code == 202:
            print("Report is being created in offline mode")
            retryIn = int(req.headers.get("retryIn", 60))
            print("Request will be resent in {} seconds".format(retryIn))
            print("RequestId:  {}".format(req.headers.get("RequestId", False)))
            sleep(retryIn)
        elif req.status_code == 500:
            print("Error occurred when creating the report. Please repeat the request again later")
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            print("JSON code for the server's response: \n{}".format(u(req.json())))
            break
        elif req.status_code == 502:
            print("Exceeded the server limit on report creation time.")
            print("Please try changing the request parameters: reduce the time period and the amount of data requested.")
            print("JSON code for the request: {}".format(body))
            print("RequestId: {}".format(req.headers.get("RequestId", False)))
            print("JSON code for the server's response: \n{}".format(u(req.json())))
            break
        else:
            print("Unexpected error")
            print("RequestId:  {}".format(req.headers.get("RequestId", False)))
            print("JSON code for the request: {}".format(body))
            print("JSON code for the server's response: \n{}".format(u(req.json())))
            break

    # Error handling if the connection with the Yandex.Direct API server wasn't established
    except ConnectionError:
        # In this case, we recommend repeating the request again later
        print("Error connecting to the Yandex.Direct API server")
        # Forced exit from loop
        break

    # If any other error occurred
    except:
        # In this case, you should analyze the application's actions
        print("Unexpected error")
        # Forced exit from loop
        break