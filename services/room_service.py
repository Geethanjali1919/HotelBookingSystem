from utils.dynamodb_handler import add_room, get_room, list_rooms
from utils.lambda_invoker import invoke_check_availability
from models.room import Room

class RoomService:
    def create_room(self, room_id, room_data):
        """
        Creates a new room entry in DynamoDB.
        
        Parameters:
        room_id (str): Unique ID for the room.
        room_data (dict): Details about the room.
        """
        # Convert Room object to dictionary if it's provided as an object
        if isinstance(room_data, Room):
            room_data = room_data.to_dict()
        
        # Add the room to DynamoDB
        add_room(room_id, room_data)

    def get_room_details(self, room_id):
        """
        Retrieves details of a specific room.
        
        Parameters:
        room_id (str): Unique ID for the room.
        
        Returns:
        Room: Room object with the details.
        """
        # Fetch room data from DynamoDB
        room_data = get_room(room_id)
        if room_data:
            return Room.from_dict(room_data)
        return None

    def get_all_rooms(self):
        """
        Retrieves a list of all available rooms.
        
        Returns:
        list: List of Room objects.
        """
        # Fetch all rooms from DynamoDB
        rooms_data = list_rooms()
        return [Room.from_dict(room) for room in rooms_data]

    def check_room_availability(self, room_id, check_in, check_out):
        """
        Checks if a room is available for specified dates by invoking a Lambda function.
        
        Parameters:
        room_id (str): Unique ID for the room.
        check_in (str): Check-in date.
        check_out (str): Check-out date.
        
        Returns:
        dict: Availability result from Lambda function.
        """
        # Invoke Lambda to check availability
        return invoke_check_availability(room_id, check_in, check_out)
