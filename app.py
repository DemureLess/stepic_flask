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

    depart_city = {}
    depart_meta = []
    nights = []

    for x in tours.keys():
        if tours[x]["departure"] == direction:
            depart_city[x] = tours[x]
            depart_meta.append(tours[x]['price'])
            nights.append(tours[x]['nights'])
    print(tours)

    #print(depart_city)

    return render_template('direction.html', departures=departures, tours=depart_city)


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

