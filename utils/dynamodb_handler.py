import boto3
from config import DYNAMODB_ROOM_TABLE, DYNAMODB_BOOKING_TABLE, DYNAMODB_USER_TABLE

dynamodb = boto3.resource('dynamodb')
rooms_table = dynamodb.Table(DYNAMODB_ROOM_TABLE)
bookings_table = dynamodb.Table(DYNAMODB_BOOKING_TABLE)
users_table = dynamodb.Table(DYNAMODB_USER_TABLE)

def create_table(table_name, key_schema, attribute_definitions):
    dynamodb = boto3.client('dynamodb')
    existing_tables = dynamodb.list_tables()['TableNames']
    if table_name not in existing_tables:
        dynamodb.create_table(
            TableName=table_name,
            KeySchema=key_schema,
            AttributeDefinitions=attribute_definitions,
            ProvisionedThroughput={'ReadCapacityUnits': 5, 'WriteCapacityUnits': 5}
        )
        print(f"DynamoDB table {table_name} created.")
    else:
        print(f"DynamoDB table {table_name} already exists.")

def add_room(room_id, room_data):
    """
    Adds a new room entry to DynamoDB.
    
    Parameters:
    room_id (str): Unique ID for the room.
    room_data (dict): Room details.
    """
    rooms_table.put_item(Item={'RoomID': room_id, **room_data})

def get_room(room_id):
    """
    Retrieves room details by room ID.
    
    Parameters:
    room_id (str): Unique ID for the room.
    
    Returns:
    dict: Room details.
    """
    response = rooms_table.get_item(Key={'RoomID': room_id})
    return response.get('Item')

def list_rooms():
    """
    Lists all rooms available in the database.
    
    Returns:
    list: List of rooms.
    """
    response = rooms_table.scan()
    return response.get('Items', [])

def create_booking(booking_data):
    """
    Adds a new booking entry to DynamoDB.
    
    Parameters:
    booking_data (dict): Booking details.
    """
    bookings_table.put_item(Item=booking_data)

def get_booking(booking_id):
    """
    Retrieves booking details by booking ID.
    
    Parameters:
    booking_id (str): Unique ID for the booking.
    
    Returns:
    dict: Booking details.
    """
    response = bookings_table.get_item(Key={'BookingID': booking_id})
    return response.get('Item')
def create_user(user_data):
    """
    Adds a new user to the UsersTable.
    
    Parameters:
    user_data (dict): User details.
    """
    table = dynamodb.Table(DYNAMODB_USER_TABLE)
    table.put_item(Item=user_data)

def get_user_by_email(email):
    """
    Fetches a user by their email.
    
    Parameters:
    email (str): User's email address.
    
    Returns:
    dict: User details if found, None otherwise.
    """
    table = dynamodb.Table(DYNAMODB_USER_TABLE)
    response = table.get_item(Key={'UserID': email})
    return response.get('Item')

def get_user_by_id(user_id):
    """
    Fetches a user by their unique user ID.
    
    Parameters:
    user_id (str): User's unique ID.
    
    Returns:
    dict: User details if found, None otherwise.
    """
    table = dynamodb.Table(DYNAMODB_USER_TABLE)
    response = table.get_item(Key={'UserID': user_id})
    return response.get('Item')