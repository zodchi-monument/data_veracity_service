# Third party import
from sklearn.covariance import EllipticEnvelope
import pandas as pd
import numpy as np
import pickle

# Local application imports
from libs.logs import logger


class Collection:

    def __init__(self, conf):
        self._collection = {}
        for k in conf:
            tags = conf[k]["tags"]
            params = conf[k]["params"]
            for t in tags:
                self._collection[t] = Model(t, params)

    def run(self, data, mode):
        ret = {}
        if mode == 'fit':
            for k in self._collection:
                logger.info(f'{k}\t: -----')
                ret[k] = self._collection[k].run(None, 'fit')
        elif mode == 'predict':
            for k in data:
                logger.info(f'{k}\t: -----')
                model = self._collection.get(k)
                if not model:
                    model = self._collection.get(k.replace("С","C"))

                if model:
                    ret[k] = model.run(data[k], 'predict')
                else:
                    ret[k] = "Not valid tag name. Tag is not in init.yaml"
                    logger.info(f'{k}\t: {ret[k]}')
        return ret


class Model:

    def __init__(self, tag, conf):
        self.tag, self.type = tag, conf["type"]
        self.zero_switch = conf.get("zero_switch")
        self.fitpath = "fitdata.csv"
        self.model = None
        self.sgm = None
        self.m = None

    def _set_from_pkl(self, path):
        self.model = pickle.load(open(path, 'rb'))

    def _chebishev(self, df):
        m, sgm = self.m, self.sgm
        d = df[df.p == 1]
        for i in d.index:
            x = d.loc[i].v
            dx = abs(m - x)
            a = (sgm ** 2 / (dx ** 2)) * 100
            d.p.loc[i] = 100 if a > 100 else a
        df.loc[df.p == 1] = d
        return df

    def run(self, data, mode):
        if mode == 'fit':

            logger.info(f'{self.tag}\t: Reading data from {self.fitpath}')

            # Считывание данных из csv и выбор интересующего тега
            dat = pd.read_csv(self.fitpath)
            # TODO: Артефакт из jupyter val->v. при рефакторинге подчистить.
            dat = dat.rename({"val": "v"}, axis=1)

            # пока проверка только на С
            с_tag = self.tag if self.tag in dat['tag'] else self.tag.replace("C","С")

            dat = dat[(dat['tag'] == self.tag)]
            df = pd.DataFrame(dat.interpolate().v)
            # Нули не рассматриваются
            if self.zero_switch:
                df = df[df > 0].dropna()
            X = df.to_numpy().reshape(-1, 1)

            logger.info(f'{self.tag}\t: Starting model fit')

            try:
                # Обучаем модель для определения характеристик распределения данных - среднего и сигмы
                self.model = EllipticEnvelope(support_fraction=1).fit(df.to_numpy())
                mask = ~(self.model.predict(X).reshape(-1, 1).squeeze() - 1).astype(bool)
                new = (X.squeeze() * mask)
                new = new[new != 0]
                self.sgm, self.m = new.std(), new.mean()
                ret = {"m": self.m, "sgm": self.sgm}

                logger.info(f"{self.tag}\t: Model fitted.")

            except ValueError as e:
                v = np.unique(X.squeeze())
                if len(v)==0:
                    e = "No tag in fit.csv"
                if len(v)==1:
                    e = "fit.csv contains single value"
                logger.error(f"{self.tag}\t: Not fitted: {str(e)}")
                logger.debug(f"{self.tag}\t: Unique values: {v}")
                ret = {"error": str(e), "model": {"m": self.m, "sgm": self.sgm}}

            logger.debug(f"{self.tag}\t: Mean = {self.m}, sigma = {self.sgm}")

        elif mode == 'predict':

            logger.info(f'{self.tag}\t: Predicting for {data}')

            # Если модель обучена
            if self.zero_switch and np.unique(data) == 0:
                ret = pd.DataFrame({"v": data, "p": np.zeros(len(data))+100}).to_json(orient="records")
            elif self.model is not None:
                # Подготовка данных для передачу в модель
                v = np.array(data).reshape(-1, 1)
                # Получение маски 100% или 0% и формирование единого DF
                msk = ~(self.model.predict(v).reshape(-1, 1).squeeze() - 1).astype(bool)
                if self.zero_switch:
                    for i in range(len(data)):
                        if data[i]==0:
                            msk[i]=100
                v = pd.DataFrame({"v": data, "p": msk})
                v.p = v.p.astype(int)

                if self.type == "chebishev":
                    logger.info(f'{self.tag}\t: Using Chebishev equation')
                    v = self._chebishev(v)
                    if self.zero_switch:
                        v['p'][v['v']==0]=100
                    ret = self._chebishev(v).to_json(orient="records")

                    logger.debug(f"{self.tag}\t: Prediction result - {ret}")
                else:
                    logger.error(f'{self.type} is not implemented yet!')
                    ret = f"{self.type} is not implemented"
            else:
                logger.error("Model is not fitted yet")
                ret = "Model is not fitted yet"

        return ret
