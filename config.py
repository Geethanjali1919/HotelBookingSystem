import os

# AWS S3 Configuration
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'hotel-booking-assets')

# DynamoDB Table Names
DYNAMODB_ROOM_TABLE = os.getenv('DYNAMODB_ROOM_TABLE', 'RoomsTable')
DYNAMODB_BOOKING_TABLE = os.getenv('DYNAMODB_BOOKING_TABLE', 'BookingsTable')
DYNAMODB_USER_TABLE = os.getenv('DYNAMODB_USER_TABLE', 'UsersTable')

# SQS Configuration
SQS_QUEUE_URL = os.getenv('SQS_QUEUE_URL', 'https://sqs.us-east-1.amazonaws.com/730335484499/BookingRequestsQueue')

# SNS Configuration
SNS_TOPIC_ARN = os.getenv('SNS_TOPIC_ARN', 'arn:aws:sns:us-east-1:730335484499:BookingNotifications')

# Lambda Function Names
LAMBDA_FUNCTION_NAME_CHECK_AVAILABILITY = os.getenv('LAMBDA_FUNCTION_NAME_CHECK_AVAILABILITY', 'CheckAvailabilityFunction')
LAMBDA_FUNCTION_NAME_PROCESS_BOOKING = os.getenv('LAMBDA_FUNCTION_NAME_PROCESS_BOOKING', 'ProcessBookingFunction')

# Flask Configuration
SECRET_KEY = os.getenv('SECRET_KEY', 'BQc54SnhcJbVi85exxO2IJh/aJXTYaobCcoAliV6')
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'