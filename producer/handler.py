import os
import json
import uuid
import time

import boto3

TOPIC_ARN = os.environ.get('TOPIC_ARN', None)  # can be provided by SAM env variable

sns = boto3.client('sns')

def create_order_payload(customer_id: str, items: list, amount: float):
    return {
        "orderId": str(uuid.uuid4()),
        "customerId": customer_id,
        "items": items,
        "amount": amount,
        "status": "CREATED",
        "createdAt": int(time.time())
    }

def publish_order(order_payload: dict):
    if not TOPIC_ARN:
        raise RuntimeError('TOPIC_ARN not configured in environment variables')
    response = sns.publish(
        TopicArn=TOPIC_ARN,
        Message=json.dumps(order_payload),
        MessageAttributes={
            'eventType': {
                'DataType': 'String',
                'StringValue': 'OrderCreated'
            }
        }
    )
    return response

def lambda_handler(event, context):
    # Example Lambda entry used for manual triggering in AWS Console
    body = event.get('body')
    if body:
        payload = json.loads(body)
    else:
        # fallback example order
        payload = create_order_payload('cust-123', [{'sku':'SKU-1','qty':1}], 99.99)
    resp = publish_order(payload)
    return {
        'statusCode': 200,
        'body': json.dumps({'message':'published','snsMessageId': resp.get('MessageId')})
    }

if __name__ == '__main__':
    # CLI test
    p = create_order_payload('cli-cust', [{'sku':'S1','qty':2}], 49.9)
    print('Publishing:', p)
    print(publish_order(p))
