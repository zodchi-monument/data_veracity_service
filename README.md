# Алгоритм верификации.

Структура сервиса
------------
**Verification**\
├── **\libs**- *вспомогательные библиотеки.*\
├── **\logs**- *хранение файла с логами сервиса.*\
├── **init.yml**- *пример конф. файл для всех тегов.*\
├── **fitdata.csv** - *CSV файл, обновляемый для нового обучения модели.*\
├── **main.py** - *Запуск REST сервиса*\
├── **inout.py** - *обертка вокруг модели, для мэнеджмент потоков данных*\
├── **model.py** - *модель прогнозирования предикторов*\

Main.py 
------------
##### Запуск через переменные окружения

    VERIFICATION_INIT - Инициализация модели из файла конфигурации. Необходимо указывать всегда при запуске модели
    VERIFICATION_HOST - Хост для запуска сервиса
    VERIFICATION_PORT - Порт для запуска сервиса

**Параметры запуска**

     -c, --conffile  Инициализация модели из файла конфигурации. Необходимо указывать всегда при запуске модели
     -s, --ho      Хост для запуска сервиса
     -p, --po      Порт для запуска сервиса

**Описание запросов**

    {
        "variables": [],
        "info": {
            "name": "verification",
            "_postman_id": "45c3a640-8ca0-c42b-0df3-19d73e756dc8",
            "description": "",
            "schema": "https://schema.getpostman.com/json/collection/v2.0.0/collection.json"
        },
        "item": [
            {
                "name": "fit_verification",
                "request": {
                    "url": "http://127.0.0.1:5000/fit",
                    "method": "POST",
                    "header": [],
                    "body": {
                        "mode": "file",
                        "file": {
                            "src": "fitdata.csv"
                        }
                    },
                    "description": "Отправка данных на обучение модели"
                },
                "response": {"mode": "fit", "data": {"FC123": {"m": 35.6345925925926, "sgm": 0.2515880317560998}, "F118": {"m": 7.522733333333332, "sgm": 0.22813416130767342}, "F119": {"m": 30.55096666666666, "sgm": 1.505135663505306}, "F135": {"m": 2.214, "sgm": 0.002645751311064657}, "F37": {"m": 98.32140000000003, "sgm": 0.6883049033676879}, "F38": {"m": 108.36290000000001, "sgm": 1.21564299446836}, "FC100": {"m": 35.275833333333324, "sgm": 0.012764751814621765}, "FC125": {"m": 110.14303333333334, "sgm": 1.2468091937243537}, "FC55": {"error": "Input contains NaN, infinity or a value too large for dtype('float64').", "model": {"m": null, "sgm": null}}, "FC62": {"m": 82.13043333333334, "sgm": 3.7889305939216604}, "FC63": {"error": "Input contains NaN, infinity or a value too large for dtype('float64').", "model": {"m": null, "sgm": null}}, "FC80": {"m": 24.788166666666672, "sgm": 0.007814871862176756}, "FC81": {"m": 85.53739999999998, "sgm": 2.9643632435988687}, "FC82": {"m": 0.34900000000000003, "sgm": 5.551115123125783e-17}, "FC92": {"m": 19.73072727272727, "sgm": 0.05526726946738253}, "FC99": {"m": 37.71613333333334, "sgm": 1.171878342187825}, "FI103": {"m": 1.9441333333333337, "sgm": 0.002472964932132311}, "FI104": {"error": "Input contains NaN, infinity or a value too large for dtype('float64').", "model": {"m": null, "sgm": null}}, "FI128": {"m": 58.218333333333355, "sgm": 0.35258269321615376}, "FI57": {"m": 53.014233333333344, "sgm": 0.47511708615409304}, "FI71": {"error": "Input contains NaN, infinity or a value too large for dtype('float64').", "model": {"m": null, "sgm": null}}}}
            },
            {
                "name": "predict_verification",
                "request": {
                    "url": "http://127.0.0.1:5000/predict",
                    "method": "POST",
                    "header": [],
                    "body": {
                        "mode": "formdata",
                        "formdata": [
                            {
                                "key": "data",
                                "value": "{"FC123":[0,35.975,35.775,38.365],"FC000":[61.2267784],"FI71":[1,2,3]}",
                                "description": "",
                                "type": "text"
                            }
                        ]
                    },
                    "description": "Отправка данных на обучение модели"
                },
                "response": "{"data": {"FC123": "[{\"v\":0.0,\"p\":0.0},{\"v\":35.975,\"p\":54.6238052649},{\"v\":35.775,\"p\":100.0},{\"v\":38.365,\"p\":0.0}]", "FC000": "Not valid tag name. Tag is not in init.yaml", "FI71": "Model is not fitted yet"}, "mode": "predict"}"
            }
        ]
    }