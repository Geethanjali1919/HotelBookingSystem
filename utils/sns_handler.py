import boto3
from config import SNS_TOPIC_ARN

sns_client = boto3.client('sns')

def create_topic(topic_name):
    sns_client = boto3.client('sns')
    topics = sns_client.list_topics()['Topics']
    for topic in topics:
        if topic_name in topic['TopicArn']:
            print(f"SNS topic {topic_name} already exists.")
            return topic['TopicArn']
    response = sns_client.create_topic(Name=topic_name)
    print(f"SNS topic {topic_name} created.")
    return response['TopicArn']

def list_topics():
    return sns_client.list_topics()

def subscribe_topic(topic_arn, protocol, endpoint):
    sns_client.subscribe(TopicArn=topic_arn, Protocol=protocol, Endpoint=endpoint)

def delete_topic(topic_arn):
    sns_client.delete_topic(TopicArn=topic_arn)


def send_notification(message, subject="Booking Notification"):
    """
    Sends a notification to the SNS topic.
    
    Parameters:
    message (str): Message content.
    subject (str): Subject of the notification.
    """
    try:
        response = sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Message=message,
            Subject=subject
        )
        return response.get('MessageId')
    except Exception as e:
        print(f"Error sending notification via SNS: {e}")
        return None
