# import pandas as pd
# from app import app
# from config import db
# from models import Country, City, Rating, Room_Type, Hotel, Hotel_Room_Type  

# csv_file = 'C:/University/Web/practica_1/data/global-hotels_0.1.csv'

# df = pd.read_csv(csv_file)


# # with app.app_context():
#     # Очистка базы данных перед загрузкой (опционально)
#     # db.drop_all()
#     # db.create_all()
# def create ():
#     for _, row in df.iterrows():
#         country = Country.query.filter_by(name=row['Country']).first()
#         if not country:
#             country = Country(name=row['Country'])
#             db.session.add(country)
#             db.session.commit()

#         city = City.query.filter_by(name=row['City'], country_id=country.id).first()
#         if not city:
#             city = City(name=row['City'], country_id=country.id)
#             db.session.add(city)
#             db.session.commit()

#         rating = Rating.query.filter_by(value=row['Rating']).first()
#         if not rating:
#             rating = Rating(value=row['Rating'])
#             db.session.add(rating)
#             db.session.commit()
        
#         roomType = Room_Type.query.filter_by(name=row['Room_Type']).first()
#         if not roomType:
#             roomType = Room_Type(name=row['Room_Type'])
#             db.session.add(roomType)
#             db.session.commit()

#         hotel = Hotel(
#                 hotel_name=row['Hotel_Name'],
#                 rating_id=rating.id,
#                 score=row['Score'],
#                 city_id=city.id,
#                 country_id=country.id
#             )
#         db.session.add(hotel)
#         # db.session.flush()

#         hotel_room_type = Hotel_Room_Type(
#                 hotel_id=hotel.id,  # ID созданного отеля
#                 roomtype_id=roomType.id,  # ID типа комнаты
#                 price=row['Price'],
#                 number_reviews=row['Number_Reviews']
#             )
#         db.session.add(hotel_room_type)

#     db.session.commit()
# create()


import pandas as pd
from app import app
from config import db
from models import Country, City, Rating, Room_Type, Hotel, Hotel_Room_Type  

csv_file = 'C:/University/Web/practica_1/data/global-hotels_0.1.csv'
df = pd.read_csv(csv_file)

def create():
    with app.app_context():  # Единый контекст
        db.create_all()  # Создаём таблицы перед загрузкой


        for _, row in df.iterrows():
            # Пропускаем строки с пустыми обязательными полями
            if pd.isna(row['Country']) or pd.isna(row['City']) or pd.isna(row['Rating']):
                continue

            country = Country.query.filter_by(name=row['Country']).first()
            if not country:
                country = Country(name=row['Country'])
                db.session.add(country)
                db.session.commit()

            city = City.query.filter_by(name=row['City'], country_id=country.id).first()
            if not city:
                city = City(name=row['City'], country_id=country.id)
                db.session.add(city)
                db.session.commit()

            rating = Rating.query.filter_by(value=row['Rating']).first()
            if not rating:
                rating = Rating(value=row['Rating'])
                db.session.add(rating)
                db.session.commit()

            roomType = Room_Type.query.filter_by(name=row['Room_Type']).first()
            if not roomType:
                roomType = Room_Type(name=row['Room_Type'])
                db.session.add(roomType)
                db.session.commit()

            hotel = Hotel(
                hotel_name=row['Hotel_Name'],
                rating_id=rating.id,
                score=row['Score'],
                city_id=city.id,
                country_id=country.id
            )
            db.session.add(hotel)
            db.session.flush()  # Получаем hotel.id

            hotel_room_type = Hotel_Room_Type(
                hotel_id=hotel.id,
                roomtype_id=roomType.id,
                price=row['Price'],
                number_reviews = int(row['Number_Reviews'].replace(",", ""))
            )
            db.session.add(hotel_room_type)

            db.session.commit()  # Commit для каждой строки
            print(f"Добавлен отель: {hotel.hotel_name}")

# create()
