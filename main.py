# Standard library imports
from flask import Flask, request, json
import argparse
import yaml
import os

# Third party import

# Local application imports
from libs.logs import logger
from inout import SetIO

# Подготовка метода для передачи json
io: SetIO
app = Flask(__name__)
# Переменная для хранения внутренних ошибок сервиса
error_reason = None


def save_error_reason(reason):
    global error_reason
    error_reason = reason


# TODO: Вынести в отдельный py все хэндлеры + сделать метод для их регистрации в приложении единый.

# Обработка неверного запроса
@app.errorhandler(400)
def handle_400(e):
    return json.dumps({'error': str(e), 'reason': "Bad request"}), 400


# Обработка обращения к несуществующему ресурсу
@app.errorhandler(404)
def handle_404(e):
    return json.dumps({'error': str(e), 'reason': "URL doesn't exist"}), 404


# Обработка обращения через неверный тип HTTP запроса
@app.errorhandler(405)
def handle_405(e):
    return json.dumps({'error': str(e), 'reason': "Wrong HTTP method"}), 405


# Обработки ошибки 500
@app.errorhandler(500)
def handle_500(e):
    return json.dumps({'error': str(e), 'reason': error_reason}), 500


app.register_error_handler(400, handle_400)
app.register_error_handler(404, handle_404)
app.register_error_handler(405, handle_405)
app.register_error_handler(500, handle_500)


@app.route('/fit', methods=['POST'])
def fit():
    try:
        logger.info('------------------- Got FIT request -------------------')
        # Замена внутреннего файла csv на пришедший в теле запроса
        f = open("fitdata.csv", 'w+b')
        data = request.get_data()
        f.write(data)
        f.close()
        logger.debug(f"post request.get_data = {data}")

        # Отправка задания в модель
        return io.run(json.dumps({"mode": "fit"}))
    # TODO: Можно вынести в декоратор отдельный, чтобы легко и красиво переиспользовать в других сервисах.
    except BaseException as e:
        # Сохранение причины ошибки для передачи обработчику
        reason = str(e)
        save_error_reason(reason)
        # Логирование причины ошибки
        logger.error(reason)


@app.route('/predict', methods=['POST'])
def predict():
    try:
        logger.info('----------------- Got PREDICT request -----------------')
        logger.debug(f"request.form = {request.form}")
        jsn = json.dumps({"mode": "predict", "data": request.form['data']})
        return io.run(jsn)
    # TODO: Надо вынести в декоратор отдельный, чтобы легко и красиво переиспользовать в других сервисах.
    except BaseException as e:
        # Сохраняем причину ошибки для передачи обработчику
        reason = str(e)
        save_error_reason(reason)
        # Логирование причины ошибки
        logger.error(reason)


if __name__ == '__main__':
    # Обработка аргументов
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conffile",
                        help="set path to yaml conf file", type=str)
    parser.add_argument("-s", "--host", help="set host ip", type=str)
    parser.add_argument("-p", "--port", help="set port", type=int)
    parsed = parser.parse_args()

    conf = os.environ.get("VERIFICATION_INIT")
    host = os.environ.get("VERIFICATION_HOST")
    port = os.environ.get("VERIFICATION_PORT")

    conf = conf if conf else parsed.conffile
    host = host if host else parsed.host
    port = int(port) if port else parsed.port

    # Инициализация модели файлом конфигурации
    with open(conf, 'r') as yml:
        try:
            conf = yaml.safe_load(yml)
            io = SetIO(conf)
        except yaml.YAMLError as exc:
            logger.error(f'Error, while reading config file: {exc}')
    # Запуск API
    app.run(host=host, port=port, debug=False)
