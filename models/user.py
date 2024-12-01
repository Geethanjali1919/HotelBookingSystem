from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, name, email):
        """
        Initialize a User object.
        
        Parameters:
        user_id (str): Unique identifier for the user.
        name (str): Name of the user.
        email (str): Email of the user.
        phone (str): Phone number of the user.
        """
        self.id = user_id
        self.name = name
        self.email = email

    @classmethod
    def from_dict(cls, data):
        """
        Creates a User instance from a dictionary.
        
        Parameters:
        data (dict): Dictionary containing user details.
        
        Returns:
        User: An instance of User.
        """
        return cls(
            user_id=data['UserID'],
            name=data['Name'],
            email=data['Email'],
            phone=data['Phone']
        )

    def to_dict(self):
        """
        Converts the User instance into a dictionary format.
        
        Returns:
        dict: Dictionary containing user details.
        """
        return {
            'UserID': self.user_id,
            'Name': self.name,
            'Email': self.email,
            'Phone': self.phone
        }
