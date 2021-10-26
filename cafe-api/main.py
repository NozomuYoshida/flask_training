from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from random import choice

app = Flask(__name__)
KEY = '1234'

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/random')
def get_random_cafe():
    cafes = db.session.query(Cafe).all()
    random_cafe = choice(cafes)
    print(random_cafe)
    return jsonify(cafe=random_cafe.to_dict())


@app.route('/all')
def get_all_cafes():
    cafes = db.session.query(Cafe).all()
    cafes_data = []
    for cafe in cafes:
        cafes_data.append(cafe.to_dict())
    return jsonify(cafes=cafes_data)


@app.route('/search')
def get_cafe_at_location():
    query_location = request.args.get('loc')
    cafe = Cafe.query.filter_by(location=query_location).first()
    if cafe:
        return jsonify(cafe=cafe.to_dict())
    else:
        return jsonify(error={'Not found': 'Sorry, we don\'t have a cafe at that location.'})


# @app.route('/update-price/<cafe_id>', methods=['PATCH'])
@app.route('/update-price/<cafe_id>', methods=['PATCH', 'GET'])
def update_coffee_price(cafe_id):
    cafe_to_update = Cafe.query.get(cafe_id)
    if cafe_to_update:
        new_price = request.args.get('new_price')
        cafe_to_update.coffee_price = new_price
        db.session.commit()
        return jsonify({'success': 'Successfully updated the price.'})
    else:
        return jsonify(error={'Not found': 'Sorry a cafe with that id was not found in the database'})
        

# @app.route('/report-closed/<cafe_id>', methods=['DELETE'])
@app.route('/report-closed/<cafe_id>', methods=['DELETE', 'GET'])
def delete_cafe(cafe_id):
    key = request.args.get('api-key')
    if key == KEY:
        cafe_to_delete = Cafe.query.get(cafe_id)
        if not cafe_to_delete:
            return jsonify(error={'Not found': 'Sorry, a cafe with that id was not found in the database'}), 404
        db.session.delete(cafe_to_delete)
        db.session.commit()
        return jsonify({'success': 'Successfully deleted the cafe.'}), 200
    else:
        return jsonify(error={'Not found': 'Sorry, that is not allowed. Make sure you have the correct api_key'}), 403


if __name__ == '__main__':
    app.run(debug=True)
