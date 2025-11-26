from dataclasses import dataclass, asdict
from typing import List, Dict
import time

@dataclass
class Order:
    orderId: str
    customerId: str
    items: List[Dict]
    amount: float
    status: str = 'CREATED'
    createdAt: int = int(time.time())

    @staticmethod
    def from_dict(d):
        # Accept either string keys or nested payload from SNS
        if isinstance(d, str):
            import json
            d = json.loads(d)
        return Order(
            orderId=d.get('orderId'),
            customerId=d.get('customerId'),
            items=d.get('items', []),
            amount=d.get('amount', 0.0),
            status=d.get('status', 'CREATED'),
            createdAt=d.get('createdAt', int(time.time()))
        )

    def to_item(self):
        obj = asdict(self)
        # DynamoDB expects decimal for numbers in some SDKs, here we keep simple types
        return obj
