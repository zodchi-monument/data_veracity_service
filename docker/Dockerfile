FROM python:3.8-slim as base
WORKDIR /app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

FROM base as runtime
COPY ./ ./
EXPOSE 80
CMD python main.py --host 0.0.0.0 --port 80 -c init.yaml
