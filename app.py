from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os

host = os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/Playlister')
client = MongoClient(host=f'{host}?retryWrites=false')
db = client.get_default_database()
games = db.games

app = Flask(__name__)
""" playlists = [
    { 'title': 'Cat Videos', 'description': 'Cats acting weird' },
    { 'title': '80\'s Music', 'description': 'Don\'t stop believing!' }
] """


@app.route('/')
def playlists_index():
    """Show all games."""
    return render_template('playlists_index.html', games=games.find())


@app.route('/games/<game_id>')
def playlists_show(game_id):
    """Show a single playlist."""
    game = games.find_one({'_id': ObjectId(game_id)})
    return render_template('playlists_show.html', game=game)


@app.route('/games/<game_id>/edit')  # crrnt
def playlists_edit(game_id):
    """Show the edit form for a playlist."""
    game = games.find_one({'_id': ObjectId(game_id)})
    return render_template('playlists_edit.html', game=game, title='Edit Item')


@app.route('/games/<game_id>', methods=['POST'])
def playlists_update(game_id):
    """Submit an edited item."""
    updated_playlist = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'trailers': request.form.get('videos').split()
    }
    games.update_one(
        {'_id': ObjectId(game_id)},
        {'$set': updated_playlist})
    return redirect(url_for('playlists_show', game_id=game_id))


@app.route('/games', methods=['POST'])
def playlists_submit():
    """Submit a new playlist."""
    game = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'price': request.form.get('price'),
        'videos': request.form.get('videos').split()
    }
    game_id = games.insert_one(game).inserted_id
    return redirect(url_for('playlists_show', game_id=game_id))


@app.route('/games/new')  # crnt
def playlists_new():
    """Create a new game."""
    return render_template('playlists_new.html', game={}, title='New Game')


@app.route('/games/<game_id>/delete', methods=['POST'])
def playlists_delete(game_id):
    """Delete one playlist."""
    games.delete_one({'_id': ObjectId(game_id)})
    return redirect(url_for('playlists_index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
