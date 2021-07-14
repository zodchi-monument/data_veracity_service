# Standard library imports
import warnings
import json
import sys
import os

import pickle

# Local application imports
from libs.logs import logger
from model import Collection


class AbsIO:
    """ Класс обеспецивает управление входным и выходным потоками для моделей"""

    def __init__(self, conf):
        self._configure()
        self.task_jsn = None
        self.models = Collection(conf=conf)

    def _configure(self):
        """ Конфигурирование сервиса """
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
        warnings.filterwarnings("ignore")

    # def set_from_pkl(self):
    #     self.models._set_from_pkl(path)

    def _run_as_task(self, model_mode, model_data):
        # HINT: Здесь может быть обертка с асинхронностью
        return self.models.run(model_data, model_mode)

    def run(self):
        model_mode, model_data = self.task_jsn["mode"], self.task_jsn.get("data")
        self.task_jsn["data"] = self._run_as_task(model_mode, model_data)
        logger.info("Finishing the procedure")
        jsn = json.dumps(self.task_jsn)
        logger.debug(f"Resulting json : {jsn}")
        return jsn


class StdIO(AbsIO):
    """ Класс реализует AbsIO для работы с stin и stdout (БЦМ)"""
    # TODO: При необходимост использовать с БЦМ - не оттестирован на коллекции
    def _configure(self):
        super()._configure()

    def run(self):
        while True:
            try:
                self.task_jsn = json.loads(sys.stdin.readline())
                super().run()
            except json.decoder.JSONDecodeError:
                pass
            except KeyboardInterrupt:
                exit()


class FileIO(AbsIO):
    """ Класс реализует AbsIO для работы с файлом"""
    # TODO: При необходимост использовать с файлом - не оттестирован на коллекции
    def __init__(self, file_name, conf):
        super().__init__(conf)
        self.file_name = file_name

    def run(self):
        for task_jsn in open(self.file_name, 'r'):
            self.task_jsn = json.loads(task_jsn)
            super().run()


class SetIO(AbsIO):
    """ Класс реализует AbsIO для работы через REST запросы"""
    def __init__(self, conf):
        super().__init__(conf)

    def run(self, jsn):
        try:
            logger.info('Parsing task json')
            self.task_jsn = json.loads(jsn)
            if self.task_jsn.get("data"):
                logger.debug(self.task_jsn["data"])
                self.task_jsn["data"] = json.loads(self.task_jsn["data"])
            return super().run()
        except json.decoder.JSONDecodeError:
            logger.error("Invalid task JSON format")
            logger.debug(jsn)

        except KeyboardInterrupt:
            exit()
