"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for # type: ignore
from flask_migrate import Migrate # type: ignore
from flask_swagger import swagger # type: ignore
from flask_cors import CORS # type: ignore
from utils import APIException, generate_sitemap
# from models import db, User, Character, Planet, BlogPost
from models import db, User
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
# setup_admin(app) # type: ignore

# Handle/serialize errors like a JSON object


@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints


@app.route('/')
def sitemap():
    return generate_sitemap(app)


@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200
# CHARACTERS ENDPOINTS


@app.route('/characters', methods=['GET'])
def get_all_characters():
    """Get all Star Wars characters"""
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters]), 200


@app.route('/characters/<int:character_id>', methods=['GET'])
def get_single_character(character_id):
    """Get a single character by ID"""
    character = Character.query.get(character_id)
    if character is None:
        raise APIException("Character not found", status_code=404)
    return jsonify(character.serialize()), 200


@app.route('/characters', methods=['POST'])
def create_character():
    """Create a new character"""
    request_data = request.get_json()

    # Create new character
    character = Character(
        name=request_data.get('name'),
        description=request_data.get('description'),
        birth_year=request_data.get('birth_year'),
        gender=request_data.get('gender'),
        height=request_data.get('height'),
        mass=request_data.get('mass'),
        hair_color=request_data.get('hair_color'),
        skin_color=request_data.get('skin_color'),
        eye_color=request_data.get('eye_color'),
        species=request_data.get('species', 'Human'),
        homeworld_id=request_data.get('homeworld_id')
    )

    db.session.add(character)
    db.session.commit()

    return jsonify(character.serialize()), 201

# PLANETS ENDPOINTS


@app.route('/planets', methods=['GET'])
def get_all_planets():
    """Get all Star Wars planets"""
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_single_planet(planet_id):
    """Get a single planet by ID"""
    planet = Planet.query.get(planet_id)
    if planet is None:
        raise APIException("Planet not found", status_code=404)
    return jsonify(planet.serialize()), 200


@app.route('/planets', methods=['POST'])
def create_planet():
    """Create a new planet"""
    request_data = request.get_json()

    # Create new planet
    planet = Planet(
        name=request_data.get('name'),
        description=request_data.get('description'),
        climate=request_data.get('climate'),
        terrain=request_data.get('terrain'),
        population=request_data.get('population'),
        diameter=request_data.get('diameter'),
        rotation_period=request_data.get('rotation_period'),
        orbital_period=request_data.get('orbital_period'),
        gravity=request_data.get('gravity'),
        surface_water=request_data.get('surface_water')
    )

    db.session.add(planet)
    db.session.commit()

    return jsonify(planet.serialize()), 201

# USERS ENDPOINTS


@app.route('/users', methods=['GET'])
def get_all_users():
    """Get all blog users"""
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200


@app.route('/users/<int:user_id>', methods=['GET'])
def get_single_user(user_id):
    """Get a single user by ID"""
    user = User.query.get(user_id)
    if user is None:
        raise APIException("User not found", status_code=404)
    return jsonify(user.serialize()), 200

# FAVORITES ENDPOINTS


@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    """Get all favorites for a specific user"""
    user = User.query.get(user_id)
    if user is None:
        raise APIException("User not found", status_code=404)

    favorites = {
        "characters": [char.serialize() for char in user.favorite_characters],
        "planets": [planet.serialize() for planet in user.favorite_planets]
    }

    return jsonify(favorites), 200


@app.route('/users/<int:user_id>/favorites/characters/<int:character_id>', methods=['POST'])
def add_favorite_character(user_id, character_id):
    """Add a character to user's favorites"""
    user = User.query.get(user_id)
    character = Character.query.get(character_id)

    if user is None:
        raise APIException("User not found", status_code=404)
    if character is None:
        raise APIException("Character not found", status_code=404)

    # Add to favorites if not already there
    if character not in user.favorite_characters:
        user.favorite_characters.append(character)
        db.session.commit()
        return jsonify({"message": "Character added to favorites"}), 200
    else:
        return jsonify({"message": "Character already in favorites"}), 200


@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['POST'])
def add_favorite_planet(user_id, planet_id):
    """Add a planet to user's favorites"""
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)

    if user is None:
        raise APIException("User not found", status_code=404)
    if planet is None:
        raise APIException("Planet not found", status_code=404)

    # Add to favorites if not already there
    if planet not in user.favorite_planets:
        user.favorite_planets.append(planet)
        db.session.commit()
        return jsonify({"message": "Planet added to favorites"}), 200
    else:
        return jsonify({"message": "Planet already in favorites"}), 200


@app.route('/users/<int:user_id>/favorites/characters/<int:character_id>', methods=['DELETE'])
def remove_favorite_character(user_id, character_id):
    """Remove a character from user's favorites"""
    user = User.query.get(user_id)
    character = Character.query.get(character_id)

    if user is None:
        raise APIException("User not found", status_code=404)
    if character is None:
        raise APIException("Character not found", status_code=404)

    if character in user.favorite_characters:
        user.favorite_characters.remove(character)
        db.session.commit()
        return jsonify({"message": "Character removed from favorites"}), 200
    else:
        return jsonify({"message": "Character not in favorites"}), 404


@app.route('/users/<int:user_id>/favorites/planets/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(user_id, planet_id):
    """Remove a planet from user's favorites"""
    user = User.query.get(user_id)
    planet = Planet.query.get(planet_id)

    if user is None:
        raise APIException("User not found", status_code=404)
    if planet is None:
        raise APIException("Planet not found", status_code=404)

    if planet in user.favorite_planets:
        user.favorite_planets.remove(planet)
        db.session.commit()
        return jsonify({"message": "Planet removed from favorites"}), 200
    else:
        return jsonify({"message": "Planet not in favorites"}), 404

# ==========================================
# END OF NEW ENDPOINTS
# ==========================================


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
