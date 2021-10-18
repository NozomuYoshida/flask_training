from flask import Flask
from random import randint

app = Flask(__name__)


def make_h1(fn):
    def wrapper(*args):
        return '<h1>' + fn() + '</h1>'
    wrapper.__name__ = fn.__name__
    return wrapper


@app.route('/')
@make_h1
def home():
    return 'Guess a number between 0 and 9<br>' \
           '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif" witdh=200px>'


target_number = randint(1, 10)


@app.route('/<int:input_number>')
# Decorator doesn't work so it's uncommented
# @make_h1
def show_result(input_number):
    if input_number == target_number:
        return f'You are right! {target_number} is the answer!'
    elif input_number > target_number:
        return f'It"s higher!'
    elif input_number < target_number:
        return f'It"s lower!'



if __name__ == '__main__':
    app.run(debug=True)from flask import Flask
from random import randint

app = Flask(__name__)


def make_h1(fn):
    def wrapper(*args):
        return '<h1>' + fn() + '</h1>'
    wrapper.__name__ = fn.__name__
    return wrapper


@app.route('/')
@make_h1
def home():
    return 'Guess a number between 0 and 9<br>' \
           '<img src="https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif" witdh=200px>'


target_number = randint(1, 10)


@app.route('/<int:input_number>')
# Decorator doesn't work so it's uncommented
# @make_h1
def show_result(input_number):
    if input_number == target_number:
        return f'You are right! {target_number} is the answer!'
    elif input_number > target_number:
        return f'It"s higher!'
    elif input_number < target_number:
        return f'It"s lower!'



if __name__ == '__main__':
    app.run(debug=True)
