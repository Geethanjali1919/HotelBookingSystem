from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from utils.dynamodb_handler import create_user, get_user_by_email, get_user_by_id

class UserService:
    def create_user(self, name, email, password):
        """
        Creates a new user in the database.
        
        Parameters:
        name (str): User's full name.
        email (str): User's email address.
        password (str): User's plain text password.
        """
        hashed_password = generate_password_hash(password)
        user_data = {
            'UserID': email,  # Use email as the unique identifier
            'Name': name,
            'Email': email,
            'Password': hashed_password
        }
        create_user(user_data)

    def authenticate_user(self, email, password):
        """
        Authenticates a user by verifying email and password.
        
        Parameters:
        email (str): User's email address.
        password (str): User's plain text password.
        
        Returns:
        User: An instance of the User class if authentication is successful, None otherwise.
        """
        user_data = get_user_by_email(email)
        if user_data and check_password_hash(user_data['Password'], password):
            return User(user_data['UserID'], user_data['Email'], user_data['Name'])
        return None

    def get_user_by_id(self, user_id):
        """
        Retrieves a user by their unique user ID.
        
        Parameters:
        user_id (str): User's unique ID.
        
        Returns:
        User: An instance of the User class if found, None otherwise.
        """
        user_data = get_user_by_id(user_id)
        if user_data:
            return User(user_data['UserID'], user_data['Email'], user_data['Name'])
        return None
