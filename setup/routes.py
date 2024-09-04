# routes.py
from flask import Blueprint, request, jsonify, Response
from flask_cors import CORS
from prometheus_client import Counter, generate_latest, Histogram, Gauge
from src.data.user.list_users import (
    ListUsersUseCase,
    ListUsersParameter
)
from src.data.user.create_user import CreateUserUseCase, CreateUserParameter
from src.data.user.get_user import GetUserUseCase, GetUserParameter
from src.data.user.delete_user import DeleteUserUseCase, DeleteUserParameter
from src.data.user.update_user import UpdateUserUseCase, UpdateUserParameter
import time

http_requests_total = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint', 'http_status'])
http_request_duration_seconds = Histogram('http_request_duration_seconds', 'HTTP request duration in seconds', ['method', 'endpoint'])
http_response_size_bytes = Histogram('http_response_size_bytes', 'HTTP response size in bytes', ['method', 'endpoint'])
exceptions_total = Counter('exceptions_total', 'Total exceptions raised', ['exception_type'])
start_time = time.time()
app_uptime_seconds = Gauge('app_uptime_seconds', 'Application uptime in seconds')
app_uptime_seconds.set_function(lambda: time.time() - start_time)

bp = Blueprint('main', __name__)
CORS(bp)

@bp.route('/', methods=['GET'])
def index():
    return (
    """
        Bem-vindo(a) ao sistema de cadastro de usuários!, 
        Por favor, acesse /users para listar, criar, atualizar ou deletar usuários.
    """
    )

@bp.route('/users', methods=['GET'])
def get_users():
    use_case = ListUsersUseCase()
    parameter = ListUsersParameter(
        name=request.args.get('name', ''),
    )
    response = use_case.proceed(parameter)
    serialized = use_case.serialize(response)        

    return jsonify(serialized)

@bp.route('/users/<id>', methods=['GET'])
def get_user(id):
    use_case = GetUserUseCase()
    parameter = GetUserParameter(id=id)
    response = use_case.proceed(parameter)
    user = use_case.serialize(response)

    return jsonify(user)

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    use_case = CreateUserUseCase()
    parameter = CreateUserParameter(
        name=data['name'],
        email=data['email'],
        last_name=data['last_name'],
        cpf=data['cpf'],
    )
    response = use_case.proceed(parameter)
    new_user = use_case.serialize(response)

    return jsonify(new_user), 201

@bp.route('/users/<id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    use_case = UpdateUserUseCase()
    parameter = UpdateUserParameter(
        id=id,
        name=data['name'],
        email=data['email'],
        cpf=data['cpf'],
        last_name=data['last_name'],
    )
    response = use_case.proceed(parameter)
    user = use_case.serialize(response)

    return jsonify(user)

@bp.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    use_case = DeleteUserUseCase()
    parameter = DeleteUserParameter(id=id)
    response = use_case.proceed(parameter)
    serialized = use_case.serialize(response)

    return jsonify(serialized), 204

@bp.route('/metrics', methods=['GET'])
def get_metrics():
    return Response(generate_latest(), mimetype='text/plain')


def increment_http_requests_total(method, success):

    if success:
        http_requests_total.labels(method, 200).inc()
    else:
        http_requests_total.labels(method, 500).inc()

@bp.before_request
def start_timer():
    request.start_time = time.time()

@bp.after_request
def record_request_data(response):
    request_latency = time.time() - request.start_time
    http_requests_total.labels(request.method, request.path, response.status_code).inc()
    http_request_duration_seconds.labels(request.method, request.path).observe(request_latency)
    http_response_size_bytes.labels(request.method, request.path).observe(len(response.data))
    return response

@bp.errorhandler(Exception)
def handle_exception(e):
    exceptions_total.labels(exception_type=type(e).__name__).inc()
    return "An error occurred: {}".format(str(e)), 500