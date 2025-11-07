from config import db
from app import app
import config as cf

class Country(db.Model):
    __tablename__ = 'Country'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('Страна', db.String(100), nullable=False)
    cities = db.relationship("City", back_populates="country", cascade='all, delete')

    def __init__(self, name):
        self.name = name


class City(db.Model):
    __tablename__ = 'City'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('Город', db.String(100), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('Country.id'))
    country = db.relationship("Country", back_populates="cities")
    hotels = db.relationship("Hotel", back_populates="city", cascade='all, delete')

    def __init__(self, name, country_id):
        self.name = name
        self.country_id = country_id


class Rating(db.Model):
    __tablename__ = 'Rating'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column('Рейтинг', db.String(50), nullable=False)
    hotels = db.relationship("Hotel", back_populates="rating", cascade='all, delete')

    def __init__(self, value):
        self.value = value


class Hotel(db.Model):
    __tablename__ = 'Hotel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hotel_name = db.Column(db.String(255), nullable=False)
    rating_id = db.Column(db.Integer, db.ForeignKey('Rating.id'))  
    score = db.Column(db.Float)
    room_type_id = db.Column(db.Integer, db.ForeignKey('Room_Type.id'))  
    city_id = db.Column(db.Integer, db.ForeignKey('City.id'))
    country_id = db.Column(db.Integer, db.ForeignKey('Country.id'))

    city = db.relationship("City", back_populates="hotels")
    rating = db.relationship("Rating", back_populates="hotels")
    hotel_room_types = db.relationship("Hotel_Room_Type", back_populates="hotel")

class Room_Type(db.Model):
    __tablename__ = 'Room_Type'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)  # Убрали 'Тип комнаты'

    hotel_room_types = db.relationship(
        "Hotel_Room_Type",
        back_populates="room_type",
        cascade='all, delete'
    )

class Hotel_Room_Type(db.Model):
    __tablename__ = 'hotel_room_type'
    hotel_id = db.Column(db.Integer, db.ForeignKey('Hotel.id'), primary_key=True)
    roomtype_id = db.Column(db.Integer, db.ForeignKey('Room_Type.id'), primary_key=True)
    price = db.Column(db.Float)
    number_reviews = db.Column(db.String(50))

    hotel = db.relationship("Hotel", back_populates="hotel_room_types")
    room_type = db.relationship("Room_Type", back_populates="hotel_room_types")


# Создание всех таблиц
cf.app.app_context().push()
with app.app_context():
    db.create_all()
