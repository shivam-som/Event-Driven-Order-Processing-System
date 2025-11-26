import os
import json
import boto3
from shared.order import Order

ORDERS_TABLE = os.environ.get('ORDERS_TABLE')
dynamodb = boto3.resource('dynamodb')

def process_record(record):
    # SQS record body will contain SNS message -> SNS wraps original message in 'Message' field
    body = record.get('body')
    try:
        payload = json.loads(body)
        # If SNS delivered message, payload may contain 'Message' field which is a JSON string
        if isinstance(payload, dict) and 'Message' in payload:
            message = payload['Message']
            try:
                event = json.loads(message)
            except Exception:
                event = message
        else:
            event = payload
    except Exception:
        event = body
    order = Order.from_dict(event)
    table = dynamodb.Table(ORDERS_TABLE)
    # idempotency: put_item with condition expression can be used; here we do a simple put
    table.put_item(Item=order.to_item())
    return order.orderId

def lambda_handler(event, context):
    records = event.get('Records', [])
    processed = []
    for r in records:
        try:
            oid = process_record(r)
            processed.append(oid)
        except Exception as e:
            print('Error processing record', e)
            # Let the Lambda fail for SQS to handle retry / DLQ as configured
            raise
    return {'processed': processed}
