from flask import Flask, render_template, abort
# from data import tours, title, subtitle, description, departures
import json

with open("data.json", "r", encoding="utf-8") as f:
     f = f.read()
     data = json.loads(f)

meta = data["meta"]
promo = data["promo"]
departures = data["departures"]
tours = data["tours"]

app = Flask(__name__)

@app.route('/')
def main():
    return render_template('index.html', promo=promo, departures=departures, tours=tours)

@app.route('/from/<direction>')
def from_direction(direction):

    depart_meta = {} # Результирующий словарь с метаданными
    depart_tour = {} # Отфильтрованный список туров
    depart_price = [] # Для сортировки  цены
    depart_nights = [] # для сортировки ночей

    for x in tours.keys():
        if tours[x]["departure"] == direction:
            depart_tour[x] = tours[x]
            depart_price.append(tours[x]['price'])
            depart_nights.append(tours[x]['nights'])

    depart_meta['depart_rus'] = departures.get(direction)
    depart_meta['direction'] = direction

    depart_meta['count'] = len(depart_tour)


    depart_price.sort()   # Минимум . максимум цены
    depart_meta['max_price'] = depart_price[-1]
    depart_meta['min_price'] = depart_price[0]

    depart_nights.sort()  # Минимум . максимум ночей
    depart_meta['max_nights'] = depart_nights[-1]
    depart_meta['min_nights'] = depart_nights[0]



    print(depart_meta)

    return render_template('direction.html', departures=departures, tours=depart_tour, meta=depart_meta)


@app.route('/tours/<id>')
def toursid(id):

    tour = tours.get(id)
    depart = tour.get('departure')
    tour['depart_rus'] = departures.get(depart)

    print(tour)

    if not tour:
        abort(404)
    else:
        return render_template('tour.html', tours=tour, departures=departures)


if __name__ == '__main__':
    app.run(debug=True)

