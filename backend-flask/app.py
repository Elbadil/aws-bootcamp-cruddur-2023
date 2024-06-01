from flask import Flask, jsonify, abort
from flask import request
from flask_cors import CORS, cross_origin
import os
from datetime import datetime, timedelta
# Flask AWS Cognito
from lib.cognito_jwt_token import CognitoJwtToken, extract_access_token, TokenVerifyError

from services.home_activities import *
from services.notifications_activities import *
from services.user_activities import *
from services.create_activity import *
from services.create_reply import *
from services.search_activities import *
from services.message_groups import *
from services.messages import *
from services.create_message import *
from services.show_activity import *
from services.users_short import *

# HoneyComb -----
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# X-Ray -------
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

# CloudWatch Logs ------
import watchtower
import logging
from time import strftime

# Rollbar -------
import os
import rollbar
import rollbar.contrib.flask
import rollbar.contrib.flask
from rollbar.contrib.flask import report_exception
from flask import got_request_exception

# HoneyComb -----
# Initialize tracing and an exporter that can send data to Honeycomb
# provider = TracerProvider()
# processor = BatchSpanProcessor(OTLPSpanExporter())
# provider.add_span_processor(processor)
# trace.set_tracer_provider(provider)
# tracer = trace.get_tracer(__name__)

app = Flask(__name__)

# X-Ray -------
# xray_url = os.getenv("AWS_XRAY_URL")
# xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)
# XRayMiddleware(app, xray_recorder)

# HoneyComb -----
# Initialize automatic instrumentation with Flask
# FlaskInstrumentor().instrument_app(app)
# RequestsInstrumentor().instrument()

# Rollbar ----
# def init_rollbar(app):
#     rollbar_access_token = os.getenv('ROLLBAR_ACCESS_TOKEN')
#     flask_env = os.getenv('FLASK_ENV')
#     if rollbar_access_token:
#         rollbar.init(
#             # access token
#             rollbar_access_token,
#             # environment name
#             flask_env,
#             # server root directory, makes tracebacks prettier
#             root=os.path.dirname(os.path.realpath(__file__)),
#             # flask already sets up logging
#             allow_logging_basic_config=False
#         )
#         # send exceptions from `app` to Rollbar, using Flask's signal system.
#         got_request_exception.connect(report_exception, app)
#         return rollbar
#     else:
#         print("No Rollbar access token provided. Error tracking disabled.")
#         return None

# rollbar = init_rollbar(app)

# @app.route('/rollbar/test')
# def rollbar_test():
#     rollbar.report_message('Hello World!', 'warning')
#     return "Hello World!"

# Configuring Logger to Use CloudWatch
# LOGGER = logging.getLogger(__name__)
# LOGGER.setLevel(logging.DEBUG)
# console_handler = logging.StreamHandler()
# cw_handler = watchtower.CloudWatchLogHandler(log_group='cruddur')
# LOGGER.addHandler(console_handler)
# LOGGER.addHandler(cw_handler)
# LOGGER.info('Test log')

frontend = os.getenv('FRONTEND_URL')
backend = os.getenv('BACKEND_URL')
origins = [frontend, backend]
cors = CORS(
  app, 
  resources={r"/api/*": {"origins": origins}},
  # expose_headers="location,link",
  # allow_headers="content-type,if-modified-since",
  headers=['Content-Type', 'Authorization'], 
  expose_headers='Authorization',
  methods="OPTIONS,GET,HEAD,POST"
)

# @app.after_request
# def after_request(response):
#   timestamp = strftime('[%Y-%b-%d %H:%M]')
#   LOGGER.error('%s %s %s %s %s %s', timestamp, request.remote_addr, request.method, request.scheme, request.full_path, response.status)
#   return response

# Connecting to our Cognito User Pool using CognitoJwtToken from lib/cognito_jwt_token.py
cognito_jwt_token = CognitoJwtToken(
  user_pool_id=os.getenv("AWS_USER_POOLS_ID"), 
  user_pool_client_id=os.getenv("AWS_USER_POOLS_CLIENT_ID"),
  region=os.getenv("AWS_DEFAULT_REGION")
)

def cognito_user_id(request_headers):
    """Verifies access token and returns the request user's
    cognito_id"""
    access_token = extract_access_token(request_headers)
    try:
        claims = cognito_jwt_token.verify(access_token)
        # authenticated request
        print("authenticated")
        # print(claims)
        # print(claims['sub'])
        cognito_user_id = claims['sub']
        return cognito_user_id
    except TokenVerifyError as e:
        # unauthenticated request
        print(e)
        print("unauthenticated")
        abort(401)

@app.route("/api/message_groups", methods=['GET'])
def data_message_groups():
    user_sub = cognito_user_id(request.headers)
    model = MessageGroups.run(cognito_user_id=user_sub)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200

@app.route("/api/messages/<string:message_group_uuid>", methods=['GET'])
def data_messages(message_group_uuid):
    # user_sub = cognito_user_id(request.headers)
    model = Messages.run(
    #    cognito_user_id=user_sub,
       message_group_uuid=message_group_uuid
    )
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200

@app.route("/api/messages", methods=['POST','OPTIONS'])
@cross_origin()
def data_create_message():
    user_sub = cognito_user_id(request.headers)
    message = request.json['message']
    message_group_uuid = request.json.get('message_group_uuid', None)
    if message_group_uuid is None:
       user_receiver_handle = request.json['handle']
    model = CreateMessage.run(message=message,
                                cognito_user_id=user_sub,
                                message_group_uuid=message_group_uuid,
                                user_receiver_handle=user_receiver_handle)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200

@app.route("/api/activities/home", methods=['GET'])
def data_home():
    # user_sub = cognito_user_id(request.headers)
    data = HomeActivities.run()
    return data, 200

@app.route('/api/users/@<string:handle>/short', methods=['GET'])
def data_user(handle):
    """"""
    model = UserShort.run(handle)
    if model['errors'] is not None:
        return model['errors'], 422
    else:
        return model['data'], 200

# Added notifications endpoint
@app.route("/api/activities/notifications", methods=['GET'])
def data_activity():
  data = NotificationsActivities.run()
  return data, 200


@app.route("/api/activities/@<string:handle>", methods=['GET'])
def data_handle(handle):
  model = UserActivities.run(handle)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200

@app.route("/api/activities/search", methods=['GET'])
def data_search():
  term = request.args.get('term')
  model = SearchActivities.run(term)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200


@app.route("/api/activities", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities():
    user_sub = cognito_user_id(request.headers)
    message = request.json.get('message')
    expires_at = request.json.get('ttl')
    user_activity = CreateActivity.run(user_sub, message, expires_at)
    if user_activity['errors'] is not None:
        return user_activity['errors'], 422
    return user_activity['data'], 200

@app.route("/api/activities/<string:activity_uuid>", methods=['GET'])
def data_show_activity(activity_uuid):
  data = ShowActivity.run(activity_uuid=activity_uuid)
  return data, 200

@app.route("/api/activities/<string:activity_uuid>/reply", methods=['POST','OPTIONS'])
@cross_origin()
def data_activities_reply(activity_uuid):
  user_handle  = 'andrewbrown'
  message = request.json['message']
  model = CreateReply.run(message, user_handle, activity_uuid)
  if model['errors'] is not None:
    return model['errors'], 422
  else:
    return model['data'], 200


if __name__ == "__main__":
  app.run(debug=True)