from models.review import Review
from models.amenity import Amenity
import models
from os import getenv
from models.base_model import Base, BaseModel
from sqlalchemy import Column, ForeignKey, String, Integer, Float, Table
from sqlalchemy.orm import relationship

if getenv("HBNB_TYPE_STORAGE") == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 primary_key=True,
                                 nullable=False),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 primary_key=True,
                                 nullable=False))


class Place(BaseModel, Base):
    """Place class that creates places table"""
    if getenv("HBNB_TYPE_STORAGE") == 'db':
        __tablename__ = "places"
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)

    else:
        city_id = ''
        user_id = ''
        name = ''
        description = ''
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.00
        longitude = 0.00

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """ Review Getter attribute in case of file storage """
            reviews_list = []

            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    reviews_list.append(review)
            return reviews_list

        @property
        def amenities(self):
            """getter"""
            amenities_list = []

            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amenities_list.append(amenity)
            return amenities_list

        @amenities.setter
        def amenities(self, obj):
            """Function that handles append method for adding an amenity"""
            if type(obj) == Amenity:
                self.amenity_ids.append(obj.id)
    else:
        reviews = relationship('Review', backref='place',
                               cascade='all, delete, delete-orphan')
        amenities = relationship("Amenity",
                                 secondary='place_amenity',
                                 back_populates='place_amenities',
                                 viewonly=False)
