import boto3
import json
from config import LAMBDA_FUNCTION_NAME_CHECK_AVAILABILITY, LAMBDA_FUNCTION_NAME_PROCESS_BOOKING

lambda_client = boto3.client('lambda')

def create_function(function_name, role, handler, code, runtime="python3.8"):
    lambda_client.create_function(
        FunctionName=function_name,
        Runtime=runtime,
        Role=role,
        Handler=handler,
        Code={'ZipFile': code}
    )

def list_functions():
    return lambda_client.list_functions()

def invoke_function(function_name, payload):
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',
        Payload=json.dumps(payload)
    )
    return json.loads(response['Payload'].read())

def update_function_code(function_name, new_code):
    lambda_client.update_function_code(FunctionName=function_name, ZipFile=new_code)

def delete_function(function_name):
    lambda_client.delete_function(FunctionName=function_name)

def invoke_check_availability(room_id, check_in, check_out):
    """
    Invokes the check availability Lambda function.
    
    Parameters:
    room_id (str): Room ID to check availability.
    check_in (str): Check-in date.
    check_out (str): Check-out date.
    
    Returns:
    dict: Response from Lambda function.
    """
    payload = json.dumps({
        'room_id': room_id,
        'check_in': check_in,
        'check_out': check_out
    })
    response = lambda_client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME_CHECK_AVAILABILITY,
        InvocationType='RequestResponse',
        Payload=payload
    )
    return json.loads(response['Payload'].read())

def invoke_process_booking(booking_data):
    """
    Invokes the process booking Lambda function.
    
    Parameters:
    booking_data (dict): Booking details.
    
    Returns:
    dict: Response from Lambda function.
    """
    payload = json.dumps(booking_data)
    response = lambda_client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME_PROCESS_BOOKING,
        InvocationType='RequestResponse',
        Payload=payload
    )
    return json.loads(response['Payload'].read())
