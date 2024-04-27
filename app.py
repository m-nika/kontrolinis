# from flask import Flask, jsonify
# import requests

# task no.1


# app = Flask(__name__)

# @app.route('/joke', methods=['GET'])
# def get_joke():
#     response = requests.get('https://official-joke-api.appspot.com/random_joke')
#     if response.status_code == 200:
#         joke = response.json()
#         setup = joke['setup']
#         punchline = joke['punchline']
#         return jsonify ({'punchline': setup, 'setup': punchline})
#     else:
#         return jsonify({'error': 'Failed to fetch joke'})
    
# if __name__ == '__main__':
#     app.run(debug=True)


# task no.2


# from flask import Flask, jsonify
# import requests

# app = Flask(__name__)
# import random

# riddles = [
#     {
#         'question': 'Give me a drink, and I will die. Feed me, and I\'ll get bigger. What am I?',
#         'answer': 'A fire'
#     },
#     {
#         'question': 'What word begins with E and ends with E, but only has one letter?',
#         'answer': 'Envelope'
#     }, 
#     {
#         'question': 'What has many rings but no fingers?', 
#         'answer': 'A telephone.'
#     }
# ]

# @app.route('/riddle', methods=['GET'])
# def get_riddle():
#     random_riddle = random.choice(riddles)
#     return jsonify({'riddle': random_riddle['answer'], 'answer': random_riddle['question']})

# if __name__ == '__main__':
#     app.run(debug=True)


# task no.3


# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/sum', methods=['POST'])
# def get_sum():
#     data = request.json
#     numbers = data['numbers']
#     total_sum = sum(numbers)
#     return jsonify({'sum': total_sum})

# if __name__ == '__main__':
#     app.run(debug=True)


# task no.4

from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/add_movie', methods=['GET'])
def show_add_movie_form():
    return render_template('add_movie.html')

@app.route('/add_movie', methods=['POST'])
def add_movie():
    data = request.form
    if not all(key in data for key in ['title', 'genre', 'rating']):
        return jsonify({'error': 'please input all required data'}), 400
    title = data['title']
    genre = data['genre']
    rating = data['rating']
    movie = Movie(title=title, genre=genre, rating=rating)
    db.session.add(movie)
    db.session.commit()
    return render_template('movie_added.html', title=title, genre=genre, rating=rating)

@app.route('/get_suggestions', methods=['GET'])
def get_suggestions():
    movies = Movie.query.order_by(Movie.rating.desc()).limit(3).all()
    if not movies:
        return jsonify({'error': 'no movies available'}), 404
    suggestions = [{'title': movie.title, 'genre': movie.genre, 'rating': movie.rating} for movie in movies]
    return jsonify(suggestions), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

