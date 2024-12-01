class Room:
    def __init__(self, room_id, name, description, price, amenities, image_url, images=None, featured=False):
        """
        Initialize a Room object.
        
        Parameters:
        room_id (str): Unique identifier for the room.
        name (str): Name of the room.
        description (str): Description of the room.
        price (float): Price per night.
        amenities (list): List of amenities available in the room.
        image_url (str): URL of the room image.
        featured (bool): Indicates if the room is featured.
        """
        self.room_id = room_id
        self.name = name
        self.description = description
        self.price = price
        self.amenities = amenities
        self.image_url = image_url
        self.images = images or [image_url]
        self.featured = featured

    @classmethod
    def from_dict(cls, data):
        """
        Creates a Room instance from a dictionary.
        
        Parameters:
        data (dict): Dictionary containing room details.
        
        Returns:
        Room: An instance of Room.
        """
        return cls(
            room_id=data['RoomID'],
            name=data['Name'],
            description=data['Description'],
            price=data['Price'],
            amenities=data['Amenities'],
            image_url=data['ImageURL'],
            images=data.get('Images'),
            featured=data.get('Featured', False)
        )

    def to_dict(self):
        """
        Converts the Room instance into a dictionary format.
        
        Returns:
        dict: Dictionary containing room details.
        """
        return {
            'RoomID': self.room_id,
            'Name': self.name,
            'Description': self.description,
            'Price': self.price,
            'Amenities': self.amenities,
            'ImageURL': self.image_url,
            'Images': self.images,
            'Featured': self.featured
        }
