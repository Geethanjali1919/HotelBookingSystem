from utils.sns_handler import send_notification

class NotificationService:
    def send_booking_confirmation(self, user_contact, booking_id):
        """
        Sends a booking confirmation notification.
        
        Parameters:
        user_contact (str): Contact information of the user (email or phone).
        booking_id (str): ID of the confirmed booking.
        
        Returns:
        str: Message ID if notification is successful.
        """
        message = f"Your booking with ID {booking_id} has been confirmed!"
        subject = "Booking Confirmation"
        return send_notification(message, subject=subject)

    def send_payment_confirmation(self, user_contact, booking_id):
        """
        Sends a payment confirmation notification.
        
        Parameters:
        user_contact (str): Contact information of the user (email or phone).
        booking_id (str): ID of the booking.
        
        Returns:
        str: Message ID if notification is successful.
        """
        message = f"Your payment for booking ID {booking_id} has been received!"
        subject = "Payment Confirmation"
        return send_notification(message, subject=subject)
