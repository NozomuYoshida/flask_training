from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///books-collection.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)


db.create_all()


@app.route('/')
def home():
    all_books = db.session.query(Book).all()
    if not all_books:
        is_empty = True
    else:
        is_empty = False
    return render_template('index.html', all_books=all_books, is_empty=is_empty)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        new_book = Book(title=request.form['title'],
                        author=request.form['author'],
                        rating=request.form['rating'])
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route('/edit', methods=["GET", "POST"])
def edit():
    book_id = request.args.get('id')
    if request.method == 'GET':
        book = Book.query.filter_by(id=book_id).first()
        print(book_id)
        return render_template('edit.html', book_to_update=book)
    elif request.method == 'POST':
        new_rating = request.form['rating']
        book_to_update = Book.query.get(book_id)
        book_to_update.rating = new_rating
        db.session.commit()
    return redirect(url_for('home'))


@app.route('/delete', methods=['GET'])
def delete():
    book_id = request.args.get('id')
    book_to_delete = Book.query.get(book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))



if __name__ == "__main__":
    app.run(debug=True)
