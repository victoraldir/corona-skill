#
#  Copyright 2010-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
#  This file is licensed under the Apache License, Version 2.0 (the "License").
#  You may not use this file except in compliance with the License. A copy of
#  the License is located at
#
#  http://aws.amazon.com/apache2.0/
#
#  This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
#  CONDITIONS OF ANY KIND, either express or implied. See the License for the
#  specific language governing permissions and limitations under the License.
#
from __future__ import print_function  # Python 2/3 compatibility

import decimal
import json
import os

import boto3

IS_OFFLINE = os.environ.get('IS_OFFLINE')


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


if IS_OFFLINE:
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1', endpoint_url="http://localhost:8000")
else:
    dynamodb = boto3.resource("dynamodb", region_name='us-east-1')

tb_global_stats = os.environ["GLOBAL_STATS_TABLE"]

table = dynamodb.Table(tb_global_stats)


def create_update_globalstats(globalStatsList):
    with table.batch_writer(overwrite_by_pkeys=['country']) as batch:
        for stats in globalStatsList['countries']:
            print('stats-----', stats)
            if stats['name'] is not None:
                batch.put_item(
                    Item={
                        'country': stats['name'],
                        'continent': stats['continent'],
                        'cases': stats['cases'],
                        'deaths': stats['deaths']
                    }
                )
