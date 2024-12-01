import uuid
from utils.dynamodb_handler import create_booking, get_booking
from utils.sqs_handler import send_booking_request
from utils.lambda_invoker import invoke_process_booking

class BookingService:
    def create_booking(self, user_id, room_id, check_in, check_out):
        """
        Creates a new booking and sends a request to the booking queue.
        
        Parameters:
        user_id (str): Unique ID for the user.
        room_id (str): Unique ID for the room.
        check_in (str): Check-in date.
        check_out (str): Check-out date.
        
        Returns:
        dict: Confirmation details if booking is successful.
        """
        # Generate a unique booking ID
        booking_id = str(uuid.uuid4())
        
        # Create booking data
        booking_data = {
            'BookingID': booking_id,
            'UserID': user_id,
            'RoomID': room_id,
            'CheckIn': check_in,
            'CheckOut': check_out,
            'Status': 'Pending'
        }

        # Add booking to DynamoDB
        create_booking(booking_data)

        # Send booking request to SQS queue
        send_booking_request(booking_data)

        return booking_data

    def confirm_booking(self, booking_data):
        """
        Confirms a booking by invoking the Lambda function to process it.
        
        Parameters:
        booking_data (dict): Booking details.
        
        Returns:
        dict: Processed booking details with confirmation.
        """
        return invoke_process_booking(booking_data)

    def get_booking_details(self, booking_id):
        """
        Retrieves booking details by booking ID.
        
        Parameters:
        booking_id (str): Unique ID for the booking.
        
        Returns:
        dict: Booking details.
        """
        return get_booking(booking_id)
