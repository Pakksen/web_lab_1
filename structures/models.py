from config import db
from models import Country, City, Rating, Hotel, Hotel_Room_Type, Room_Type
from sqlalchemy import func, cast, Integer


def get_all_hotel():
    column_names = [
        "Название отеля", "Рейтинг", "Оценка", "Количество отзывов",
        "Стоимость", "Тип комнаты", "Страна", "Город"
    ]

    query = (
        db.session.query(
            Hotel.hotel_name.label("Название отеля"),
            Rating.value.label("Рейтинг"),
            Hotel.score.label("Оценка"),
            Hotel_Room_Type.number_reviews.label("Количество отзывов"),
            Hotel_Room_Type.price.label("Стоимость"),
            Room_Type.name.label("Тип комнаты"),
            Country.name.label("Страна"),
            City.name.label("Город"),
        )
        .select_from(Hotel)
        .join(Rating, Hotel.rating_id == Rating.id)
        .join(City, Hotel.city_id == City.id)
        .join(Country, City.country_id == Country.id)
        .join(Hotel_Room_Type, Hotel.id == Hotel_Room_Type.hotel_id)
        .join(Room_Type, Hotel_Room_Type.roomtype_id == Room_Type.id)
    )

    result = query.all()
    if not result:
        return [[], []]

    return [column_names, result]


def get_all_excellent_rated_hotels():
    column_names = [
        "Название отеля", "Рейтинг", "Оценка", "Количество отзывов",
        "Стоимость", "Тип комнаты", "Страна", "Город"
    ]

    query = (
        db.session.query(
            Hotel.hotel_name.label("Название отеля"),
            Rating.value.label("Рейтинг"),
            Hotel.score.label("Оценка"),
            Hotel_Room_Type.number_reviews.label("Количество отзывов"),
            Hotel_Room_Type.price.label("Стоимость"),
            Room_Type.name.label("Тип комнаты"),
            Country.name.label("Страна"),
            City.name.label("Город")
        )
        .select_from(Hotel)
        .join(Rating, Hotel.rating_id == Rating.id)
        .join(City, Hotel.city_id == City.id)
        .join(Country, City.country_id == Country.id)
        .join(Hotel_Room_Type, Hotel.id == Hotel_Room_Type.hotel_id)
        .join(Room_Type, Hotel_Room_Type.roomtype_id == Room_Type.id)
        .filter(Rating.value == 'Excellent')
    )

    return column_names, query.all()



def get_avg_price_by_country():
    column_names = ["Страна", "Средняя цена"]

    query = (
        db.session.query(
            Country.name.label("Страна"),
            func.avg(Hotel_Room_Type.price).label("Средняя цена")
        )
        .join(Hotel, Hotel.country_id == Country.id)
        .join(Hotel_Room_Type, Hotel.id == Hotel_Room_Type.hotel_id)
        .group_by(Country.id)
        .order_by(func.avg(Hotel_Room_Type.price).desc())
    )

    return column_names, query.all()



def get_cheapest_excellent_hotel_per_country():
    column_names = ["Название отеля", "Цена", "Страна", "Город", "Рейтинг"]

    # Подзапрос: минимальная цена для Excellent-отелей по странам
    min_price_subq = (
        db.session.query(
            Country.id.label("country_id"),
            func.min(Hotel_Room_Type.price).label("min_price")
        )
        .join(Hotel, Hotel.country_id == Country.id)
        .join(Hotel_Room_Type, Hotel.id == Hotel_Room_Type.hotel_id)
        .join(Rating, Rating.id == Hotel.rating_id)
        .filter(Rating.value == "Excellent")
        .group_by(Country.id)
        .subquery()
    )

    # Основной запрос: выбираем отели с минимальной ценой
    query = (
        db.session.query(
            Hotel.hotel_name.label("Название отеля"),
            Hotel_Room_Type.price.label("Цена"),
            Country.name.label("Страна"),
            City.name.label("Город"),
            Rating.value.label("Рейтинг")
        )
        .join(min_price_subq, Country.id == min_price_subq.c.country_id)
        .join(Hotel, Hotel.country_id == Country.id)
        .join(Hotel_Room_Type, Hotel.id == Hotel_Room_Type.hotel_id)
        .join(City, City.id == Hotel.city_id)
        .join(Rating, Rating.id == Hotel.rating_id)
        .filter(
            Rating.value == "Excellent",
            Hotel_Room_Type.price == min_price_subq.c.min_price
        )
    )

    return column_names, query.all()



def get_most_reviewed_cities():
    column_names = ["Город", "Страна", "Всего отзывов"]


    # Если number_reviews — строка с запятыми
    reviews_expr = func.replace(Hotel_Room_Type.number_reviews, ',', '')
    total_reviews = func.sum(func.cast(reviews_expr, db.Integer))

    query = (
        db.session.query(
            City.name.label("Город"),
            Country.name.label("Страна"),
            total_reviews.label("Всего отзывов")
        )
        .join(Hotel, Hotel.city_id == City.id)
        .join(Hotel_Room_Type, Hotel.id == Hotel_Room_Type.hotel_id)
        .join(Country, Country.id == City.country_id)
        .group_by(City.id, Country.name)
        .order_by(total_reviews.desc())
    )

    return column_names, query.all()



def get_country_avg_scores():
    column_names = ["Страна", "Средняя оценка"]

    avg_score = func.round(func.avg(Hotel.score), 2)

    query = (
        db.session.query(
            Country.name.label("Страна"),
            avg_score.label("Средняя оценка")
        )
        .join(Hotel, Hotel.country_id == Country.id)
        .group_by(Country.id)
        .order_by(avg_score.desc())
    )

    return column_names, query.all()


def get_hotels_room_types_reviews():
    """
    Возвращает список отелей с типами комнат и количеством просмотров,
    отсортированный по убыванию просмотров.
    
    Возвращает:
        (column_names: list, result: list of tuples)
    """
    column_names = ["Название отеля", "Тип комнаты", "Количество просмотров"]

    # Очищаем number_reviews от запятых и преобразуем в число для сортировки
    reviews_clean = func.replace(Hotel_Room_Type.number_reviews, ',', '')
    reviews_as_int = cast(reviews_clean, Integer)

    query = (
        db.session.query(
            Hotel.hotel_name.label("Название отеля"),
            Room_Type.name.label("Тип комнаты"),
            Hotel_Room_Type.number_reviews.label("Количество просмотров")
        )
        .join(Hotel_Room_Type, Hotel.id == Hotel_Room_Type.hotel_id)
        .join(Room_Type, Hotel_Room_Type.roomtype_id == Room_Type.id)
        .order_by(reviews_as_int.desc())
    )

    result = query.all()
    return column_names, result if result else []

# Создание всех таблиц
# with app.app_context():
#     db.create_all()
