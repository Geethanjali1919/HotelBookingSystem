class Booking:
    def __init__(self, booking_id, user_id, room_id, check_in, check_out, status="Pending"):
        """
        Initialize a Booking object.
        
        Parameters:
        booking_id (str): Unique identifier for the booking.
        user_id (str): Unique identifier for the user.
        room_id (str): Unique identifier for the room.
        check_in (str): Check-in date.
        check_out (str): Check-out date.
        status (str): Status of the booking (default is "Pending").
        """
        self.booking_id = booking_id
        self.user_id = user_id
        self.room_id = room_id
        self.check_in = check_in
        self.check_out = check_out
        self.status = status

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Booking instance from a dictionary.
        
        Parameters:
        data (dict): Dictionary containing booking details.
        
        Returns:
        Booking: An instance of Booking.
        """
        return cls(
            booking_id=data['BookingID'],
            user_id=data['UserID'],
            room_id=data['RoomID'],
            check_in=data['CheckIn'],
            check_out=data['CheckOut'],
            status=data.get('Status', "Pending")
        )

    def to_dict(self):
        """
        Converts the Booking instance into a dictionary format.
        
        Returns:
        dict: Dictionary containing booking details.
        """
        return {
            'BookingID': self.booking_id,
            'UserID': self.user_id,
            'RoomID': self.room_id,
            'CheckIn': self.check_in,
            'CheckOut': self.check_out,
            'Status': self.status
        }
