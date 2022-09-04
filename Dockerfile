FROM python:3.8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip wheel --wheel-dir /wheels -r requirements.txt

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* && rm -rf /wheels/

COPY . .

EXPOSE 8002

CMD ["python", "main.py"]

