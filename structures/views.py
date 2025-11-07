from app import app
from flask import render_template
from structures.models import get_all_hotel, get_all_excellent_rated_hotels, get_avg_price_by_country, get_cheapest_excellent_hotel_per_country,get_most_reviewed_cities, get_country_avg_scores, get_hotels_room_types_reviews


@app.route('/')
def index():
    [hotel_head, hotel_body] = get_all_hotel()
    [excellent_hotels_head, excellent_hotels_body] = get_all_excellent_rated_hotels()
    [avg_price_head, avg_price_body] = get_avg_price_by_country()
    [cheapest_head, cheapest_body] = get_cheapest_excellent_hotel_per_country()
    [reviewed_head, reviewed_body] = get_most_reviewed_cities()
    [scores_head, scores_body] = get_country_avg_scores()
    [reviews_head, reviews_body] = get_hotels_room_types_reviews()

    html = render_template(
        'index.html',
        hotel_head=hotel_head,
        hotel_body=hotel_body,
        excellent_hotels_head=excellent_hotels_head,
        excellent_hotels_body=excellent_hotels_body,
        avg_price_head=avg_price_head,
        avg_price_body=avg_price_body,
        cheapest_head=cheapest_head,
        cheapest_body=cheapest_body,
        reviewed_head=reviewed_head,
        reviewed_body=reviewed_body,
        scores_head=scores_head,
        scores_body=scores_body,
        reviews_head=reviews_head,
        reviews_body=reviews_body
    )

    return html