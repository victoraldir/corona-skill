from __future__ import print_function  # Python 2/3 compatibility
import boto3
import json
import decimal
import os
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError

IS_OFFLINE = os.environ.get('IS_OFFLINE')


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


if IS_OFFLINE:
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1', endpoint_url="http://localhost:8000")
else:
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')

table = dynamodb.Table('GlobalStats-dev')


# country = "China"

def get_status_by_country(country):
    print('IS_OFFLINE', IS_OFFLINE)
    try:
        response = table.get_item(
            Key={
                'country': country
            }
        )
    except ClientError as e:
        print('Something went wrong', e)
        print(e.response['Error']['Message'])
    else:
        item = response['Item']
        print("GetItem succeeded:")
        print(json.dumps(item, indent=4, cls=DecimalEncoder))
        return item
