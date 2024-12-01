from flask import Flask, render_template, request, redirect, url_for, flash
from services.room_service import RoomService
from services.booking_service import BookingService
from services.notification_service import NotificationService
from services.user_service import UserService
from models.room import Room
from models.booking import Booking
from config import SECRET_KEY, DEBUG
from datetime import datetime
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from config import DYNAMODB_ROOM_TABLE, DYNAMODB_BOOKING_TABLE, SNS_TOPIC_ARN
from utils.booking_manager import BookingManager
from utils.s3_handler import create_bucket
from utils.dynamodb_handler import create_table
from utils.sns_handler import create_topic
from utils.sqs_handler import create_queue
from config import S3_BUCKET_NAME


app = Flask(__name__)
app.secret_key = SECRET_KEY
app.debug = DEBUG

# Initialize services
room_service = RoomService()
booking_service = BookingService()
notification_service = NotificationService()
user_service = UserService()

# Setup AWS resources
def setup_aws_resources():
    # Create S3 Bucket
    print(f"Setting up S3 bucket: {S3_BUCKET_NAME}")
    create_bucket(S3_BUCKET_NAME)

    # Create DynamoDB Tables
    print("Setting up DynamoDB tables...")
    create_table(
        table_name='RoomsTable',
        key_schema=[{'AttributeName': 'RoomID', 'KeyType': 'HASH'}],
        attribute_definitions=[{'AttributeName': 'RoomID', 'AttributeType': 'S'}]
    )
    create_table(
        table_name='BookingsTable',
        key_schema=[{'AttributeName': 'BookingID', 'KeyType': 'HASH'}],
        attribute_definitions=[{'AttributeName': 'BookingID', 'AttributeType': 'S'}]
    )
    create_table(
        table_name='UsersTable',
        key_schema=[{'AttributeName': 'UserID', 'KeyType': 'HASH'}],
        attribute_definitions=[{'AttributeName': 'UserID', 'AttributeType': 'S'}]
    )

    # Create SNS Topic
    print("Setting up SNS topic...")
    create_topic("BookingNotifications")

    # Create SQS Queue
    print("Setting up SQS queue...")
    create_queue("BookingRequestsQueue")

setup_aws_resources()

booking_manager = BookingManager(
    room_table=DYNAMODB_ROOM_TABLE,
    booking_table=DYNAMODB_BOOKING_TABLE,
    sns_topic_arn=SNS_TOPIC_ARN
)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return user_service.get_user_by_id(user_id)  # Implement get_user_by_id in UserService

# Home Page
@app.route('/')
def home():
    rooms = room_service.get_all_rooms()
    featured_rooms = [room for room in rooms if room.featured]
    return render_template('home.html', rooms=featured_rooms)

@app.route('/offers')
def offers():
    offers = [
        "Stay 3 nights and get the 4th night free!",
        "Book now and enjoy a complimentary spa session.",
        "Early bird discount: 20% off for bookings made 30 days in advance."
    ]
    return render_template('offers.html', offers=offers)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = user_service.authenticate_user(email, password)  # Implement authentication logic
        if user:
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials. Please try again.", "error")

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        user_service.create_user(name, email, password)  # Implement user creation logic
        flash("Register successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "success")
    return redirect(url_for('home'))

@app.route('/terms')
def terms():
    return render_template('terms.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


# Rooms Listing Page
@app.route('/rooms')
def rooms():
    rooms = room_service.get_all_rooms()
    return render_template('rooms.html', rooms=rooms)

# Room Details Page
@app.route('/rooms/<room_id>')
def room_details(room_id):
    room = room_service.get_room_details(room_id)
    if not room:
        flash("Room not found!", "error")
        return redirect(url_for('rooms'))
    return render_template('room_details.html', room=room)

@app.route('/gallery')
def gallery():
    images = [
        "static/assets/feature1.jpg",
        "static/assets/feature2.jpg",
        "static/assets/feature3.jpg"
    ]
    return render_template('gallery.html', images=images)



# Booking Page
@app.route('/booking/<room_id>', methods=['GET', 'POST'])
@login_required
def booking(room_id):
    if request.method == 'POST':
        try:
            check_in = request.form['check_in']
            check_out = request.form['check_out']
            user_details = {
                'name': request.form['name'],
                'email': request.form['email'],
                'phone': request.form['phone']
            }

            # Use BookingManager to create a booking
            booking = booking_manager.create_booking(room_id, check_in, check_out, user_details)
            flash(f"Booking confirmed! ID: {booking['BookingID']}", "success")
            return redirect(url_for('confirmation', booking_id=booking['BookingID']))
        except ValueError as e:
            flash(str(e), "error")

    # Fetch room details for GET request
    room = room_service.get_room_details(room_id)
    if not room:
        flash("Room not found!", "error")
        return redirect(url_for('rooms'))

    return render_template('booking.html', room=room)

def calculate_total_price(price_per_night, check_in, check_out):
    check_in_date = datetime.strptime(check_in, "%Y-%m-%d")
    check_out_date = datetime.strptime(check_out, "%Y-%m-%d")
    nights = (check_out_date - check_in_date).days
    return price_per_night * nights

# Booking Confirmation Page
@app.route('/confirmation/<booking_id>')
def confirmation(booking_id):
    booking = booking_service.get_booking_details(booking_id)
    if not booking:
        flash("Booking not found!", "error")
        return redirect(url_for('home'))

    room = room_service.get_room_details(booking['RoomID'])
    total_price = calculate_total_price(room.price, booking['CheckIn'], booking['CheckOut'])

    return render_template(
        'confirmation.html',
        booking=booking,
        room=room,
        total_price=total_price
    )


@app.route('/contact')
def contact():
    # Replace with logic to display contact details
    return render_template('contact.html')


if __name__ == "__main__":
    app.run()
