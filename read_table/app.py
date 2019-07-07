import json
import boto3


def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    response = client.scan()
    return {
        "statusCode": 200,
        "body": json.dumps(response),
    }


if __name__ == "__main__":
    lambda_handler()