# Event-Driven Order Processing System    

**Description**: Designed and implemented a scalable event-driven order workflow using AWS SNS, SQS, Lambda, and DynamoDB. This project demonstrates decoupled microservices communication, improved fault tolerance, and consistent processing under high load.

<img width="1306" height="465" alt="image" src="https://github.com/user-attachments/assets/f0251a9f-f10e-4fb8-b5ba-d22d25411c89" />

## Project Structure
- `producer/` - Lambda (or local script) that publishes order events to an SNS topic.
  - `producer/handler.py` - example producer handler / script using boto3.
- `consumer/` - Lambda that processes messages from SQS (subscribed to SNS) and writes order state to DynamoDB.
  - `consumer/handler.py` - Lambda handler for processing SQS events.
- `shared/` - shared utilities and models.
  - `shared/order.py` - Order dataclass and helpers.
- `template.yaml` - AWS SAM template to deploy SNS topic, SQS queue, Lambda functions, and DynamoDB table.
- `requirements.txt` - Python dependencies for Lambdas.
- `tests/` - example local tests and event samples.

## How it works (high level)
1. `producer` publishes an `OrderCreated` event to an **SNS topic**.
2. An **SQS queue** subscribes to that SNS topic (acts as a durable buffer).
3. `consumer` Lambda is triggered by the SQS queue, processes the order event, and writes the order state to **DynamoDB**.
4. Using SNS + SQS decouples producer and consumer and provides retry/durability guarantees.

## Local testing (without AWS)
- The code uses `boto3`. For local testing you can use environment variables to point to local endpoints (e.g., LocalStack) or mock `boto3` calls with `moto`.
- Example: `AWS_ENDPOINT_URL=http://localhost:4566` for LocalStack.

## Deploy (AWS SAM)
1. Install AWS SAM CLI and AWS CLI, configure credentials.
2. Build:
   ```bash
   sam build
   ```
3. Deploy:
   ```bash
   sam deploy --guided
   ```
This will create an SNS Topic, an SQS queue subscribed to that topic, two Lambda functions (producer & consumer), and a DynamoDB table.

## Files included
- `producer/handler.py` - publish example events (can be used as a Lambda or CLI script)
- `consumer/handler.py` - SQS-triggered Lambda that processes events and writes to DynamoDB
- `shared/order.py` - order model and helper serialization
- `template.yaml` - SAM template (with IAM roles)
- `requirements.txt` - dependencies list
- `tests/sample_event.json` - example SNS/SQS event payload

## Notes & Next steps
- Add visibility timeout tuning, DLQ (dead-letter queue) configuration for the SQS queue.
- Add idempotency checks and more robust error handling for exactly-once semantics.
- Add observability (CloudWatch Metrics, X-Ray tracing, structured logs).

