import datetime
from utils.dynamodb_handler import get_room, create_booking
from utils.sns_handler import send_notification

class BookingManager:
    def __init__(self, room_table, booking_table, sns_topic_arn):
        """
        Initialize the BookingManager.

        Parameters:
        - room_table (str): Name of the DynamoDB table for rooms.
        - booking_table (str): Name of the DynamoDB table for bookings.
        - sns_topic_arn (str): ARN of the SNS topic for notifications.
        """
        self.room_table = room_table
        self.booking_table = booking_table
        self.sns_topic_arn = sns_topic_arn

    def check_availability(self, room_id, check_in, check_out):
        """
        Check if a room is available for the given date range.

        Parameters:
        - room_id (str): Unique ID of the room.
        - check_in (str): Check-in date in YYYY-MM-DD format.
        - check_out (str): Check-out date in YYYY-MM-DD format.

        Returns:
        - bool: True if the room is available, False otherwise.
        """
        room = get_room(room_id)
        if not room:
            raise ValueError(f"Room with ID {room_id} does not exist.")

        # Simulated availability check logic
        # In production, you would query existing bookings for this room
        existing_bookings = room.get('Bookings', [])
        for booking in existing_bookings:
            if (check_in <= booking['CheckOut'] and check_out >= booking['CheckIn']):
                return False
        return True

    def calculate_price(self, base_price, check_in, check_out):
        """
        Calculate the total price for the stay, applying dynamic pricing logic.

        Parameters:
        - base_price (float): Base price per night for the room.
        - check_in (str): Check-in date in YYYY-MM-DD format.
        - check_out (str): Check-out date in YYYY-MM-DD format.

        Returns:
        - float: Total price for the stay.
        """
        check_in_date = datetime.datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.datetime.strptime(check_out, '%Y-%m-%d')
        nights = (check_out_date - check_in_date).days

        # Apply seasonal pricing (example: 20% increase during peak season)
        peak_season = [12, 1, 7]  # December, January, July
        if check_in_date.month in peak_season or check_out_date.month in peak_season:
            return base_price * nights * 1.2

        return base_price * nights

    def validate_booking(self, room_id, check_in, check_out, user_details):
        """
        Validate a booking request.

        Parameters:
        - room_id (str): Unique ID of the room.
        - check_in (str): Check-in date in YYYY-MM-DD format.
        - check_out (str): Check-out date in YYYY-MM-DD format.
        - user_details (dict): Dictionary containing user details (e.g., name, email).

        Returns:
        - bool: True if the booking is valid, False otherwise.
        """
        if not self.check_availability(room_id, check_in, check_out):
            return False

        # Ensure check-in and check-out dates are valid
        check_in_date = datetime.datetime.strptime(check_in, '%Y-%m-%d')
        check_out_date = datetime.datetime.strptime(check_out, '%Y-%m-%d')
        if check_out_date <= check_in_date:
            raise ValueError("Check-out date must be after check-in date.")

        # Ensure user details are complete
        required_fields = ['name', 'email', 'phone']
        for field in required_fields:
            if field not in user_details or not user_details[field]:
                raise ValueError(f"Missing required user detail: {field}")

        return True

    def create_booking(self, room_id, check_in, check_out, user_details):
        """
        Create a new booking.

        Parameters:
        - room_id (str): Unique ID of the room.
        - check_in (str): Check-in date in YYYY-MM-DD format.
        - check_out (str): Check-out date in YYYY-MM-DD format.
        - user_details (dict): Dictionary containing user details (e.g., name, email).

        Returns:
        - dict: Booking confirmation details.
        """
        if not self.validate_booking(room_id, check_in, check_out, user_details):
            raise ValueError("Booking validation failed.")

        booking_id = f"booking-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        booking_data = {
            'BookingID': booking_id,
            'RoomID': room_id,
            'UserID': user_details['email'],
            'CheckIn': check_in,
            'CheckOut': check_out,
            'Status': 'Confirmed'
        }

        create_booking(booking_data)

        # Send notification
        self.send_booking_notification(user_details['email'], booking_id)

        return booking_data

    def send_booking_notification(self, user_email, booking_id):
        """
        Send a booking confirmation notification.

        Parameters:
        - user_email (str): Email of the user.
        - booking_id (str): ID of the confirmed booking.
        """
        message = f"Your booking with ID {booking_id} has been confirmed!"
        send_notification(message, subject="Booking Confirmation")
