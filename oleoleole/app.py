import json
import requests
import os

app_version = os.getenv("APP_VERSION")

def oleoleole(event, context):
    try:
        ip = requests.get("http://checkip.amazonaws.com/")
    except requests.RequestException as e:
        print(e)

        raise e

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Feelin' hot hot hot!",
            "version": app_version,
            "location": ip.text.replace("\n", "")
        }),
    }
