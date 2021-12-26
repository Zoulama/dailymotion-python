from flask_jsonschema_validator import JSONSchemaValidator
from flask import Flask, jsonify, request, redirect
from flask_mail import Mail, Message
import swagger
import jsonschema
import urllib.parse

from src.domain.user.user_entity import UserEntity
from src.domain.user.user_repository import UserRepository
from src.domain.user.user_service import UserService, UserNotFoundException
from src.infrastructure.storage.database.mongo_db.mongo_client import MongodbClient
from os import environ as env

import config

app = Flask(__name__, static_url_path='/static')

JSONSchemaValidator(app=app, root="schemas")
app.register_blueprint(swagger.swagger_ui_blueprint, url_prefix=swagger.SWAGGER_URL)

mongodb_client = MongodbClient()
mongodb_user_collection = mongodb_client.users
user_repository = UserRepository(mongodb_user_collection)
user_service = UserService(user_repository)

app.config['MAIL_SERVER'] = env.get("MAIL_SERVER")
app.config['MAIL_PORT'] = env.get("MAIL_PORT")
app.config['MAIL_USERNAME'] = env.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = env.get("MAIL_PASSWORD")
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)


@app.route('/')
def root_url():
    return redirect('/api/documentation/swagger')


@app.route('/v1/registration/users', methods=['POST'])
@app.validate('user', 'user_schema')
def registration():
    content = request.get_json()
    is_registered = user_service.is_registered(content['email'])

    if is_registered is True:
        return jsonify(status='fail', statusCode='404', statusDescription='user already exist'), 404
    create_user_response = user_service.create(UserEntity.from_dict(data=request.get_json()))

    response = create_user_response.to_dict()
    try:
        msg = Message(
            'Hello here is your verification code',
            sender=env.get("MAIL_USERNAME"),
            recipients=[response['email']]
        )
        msg.body = str(response['code'])
        mail.send(msg)
        return jsonify(status='success', data={'user': response})
    except Exception as e:
        return jsonify(status='fail', statusCode='4030', statusDescription=str(e)), 500


@app.route('/v1/registration/users/confirmation/<string:email>/<string:code>', methods=['GET'])
def confirmation(email: str, code: int):
    try:
        fetch_response = user_service.confirm_code(urllib.parse.unquote(email), code)
        return jsonify(status='success', data={'user': fetch_response.to_dict()})
    except UserNotFoundException as e:
        return jsonify(status='fail', statusCode='4020', statusDescription=str(e)), 404
    except Exception as e:
        return jsonify(status='fail', statusCode='4030', statusDescription=str(e)), 500


@app.errorhandler(jsonschema.ValidationError)
def on_validation_error(e):
    return jsonify(
        {"status": "error", "statusCode": "4000", "statusDescription": e.message}), 400


if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG_MODE)
