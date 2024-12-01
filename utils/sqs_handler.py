import boto3
import json
from config import SQS_QUEUE_URL

sqs_client = boto3.client('sqs')

def create_queue(queue_name):
    sqs_client = boto3.client('sqs')
    existing_queues = sqs_client.list_queues().get('QueueUrls', [])
    if any(queue_name in url for url in existing_queues):
        print(f"SQS queue {queue_name} already exists.")
        return
    sqs_client.create_queue(QueueName=queue_name)
    print(f"SQS queue {queue_name} created.")

def send_message(queue_url, message_body):
    sqs_client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message_body))

def receive_message(queue_url):
    response = sqs_client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=10)
    messages = response.get('Messages', [])
    if messages:
        message = messages[0]
        sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=message['ReceiptHandle'])
        return json.loads(message['Body'])
    return None

def delete_message(queue_url, receipt_handle):
    sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)

def send_booking_request(booking_data):
    """
    Sends a booking request to the SQS queue.
    
    Parameters:
    booking_data (dict): Booking details.
    """
    try:
        response = sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(booking_data)
        )
        return response.get('MessageId')
    except Exception as e:
        print(f"Error sending message to SQS: {e}")
        return None

def receive_booking_request():
    """
    Retrieves a booking request from the SQS queue.
    
    Returns:
    dict: Booking details.
    """
    try:
        response = sqs_client.receive_message(
            QueueUrl=SQS_QUEUE_URL,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=10
        )
        messages = response.get('Messages', [])
        if messages:
            message = messages[0]
            sqs_client.delete_message(
                QueueUrl=SQS_QUEUE_URL,
                ReceiptHandle=message['ReceiptHandle']
            )
            return json.loads(message['Body'])
        return None
    except Exception as e:
        print(f"Error receiving message from SQS: {e}")
        return None
