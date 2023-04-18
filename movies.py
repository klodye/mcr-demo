#!/bin/python

from flask import Flask, Response, request, jsonify

from Simpledatabase import SimpleDatabase


app = Flask(__name__)
db = SimpleDatabase()

BAD_REQUEST = ('Bad Request', 400)
NOT_FOUND = ('Not Found', 404)


@app.route('/movies', methods=['GET'])
def get_movies():
    """Loading whole table from database

    Returns:
        str: str reprezentation in json format of all movies
    """
    movies = db.list()
    return jsonify(movies)


@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """Load row from table with specific id

    Args:
        movie_id (int): id of movie to be returned
    """
    movie = db.get_by_id(movie_id)

#if id is not in table return ERROR
    if not movie:
        return Response(
            NOT_FOUND[0],
            status=NOT_FOUND[1]
        )

    return jsonify(movie)


@app.route('/movies', methods=['POST'])
def upload_movie():
    """Upload new movie in the table
    """
    movie = request.json

#if request does not have specific arguments return ERROR
    if not __check_post__(movie.keys()):
        return Response(
            BAD_REQUEST[0],
            status=BAD_REQUEST[1]
        )

#with correct arguments upload movie in the table
#with or without description, depends on command
    if movie.get('description', ""):
        new_movie = db.insert(
            movie.get('title'),
            movie.get('release_year'),
            movie.get('description')
        )
    else:
        new_movie = db.insert(
            movie.get('title'),
            movie.get('release_year')
        )

    return jsonify(new_movie)


@app.route('/movies/<int:movie_id>', methods=['PUT'])
def update_movie(movie_id):
    """Upload changes to the table

    Args:
        movie_id (int): id of the movie to be changed
    """
    movie = request.json

    changed_entry = db.update(movie_id, movie)

#if movie id not found in the table return ERROR
    if not changed_entry:
        return Response(
            NOT_FOUND[0],
            status=NOT_FOUND[1]
        )

    return jsonify(changed_entry)


def __check_post__(post_keys):
    """Checking if 'POST' command got right arguments

    Args:
        post_keys (List): List of keys that are nessessary
        for upload new movie

    Returns:
        Bool: If the list of keys is correct
    """
    required_keys = ('title', 'release_year')

    for key in required_keys:
        if key not in post_keys:
            return False

    return True


if __name__ == '__main__':
    app.run()
