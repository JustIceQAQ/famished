FROM python:3.8

WORKDIR /code



COPY ./requirements.txt /code/requirements.txt

RUN pip wheel --wheel-dir /wheels -r requirements.txt

RUN apt-get update && apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    --no-install-recommends \
    && curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends


RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* && rm -rf /wheels/

COPY . .

EXPOSE 8002

ENV deploy_level=prod

CMD ["python", "main.py"]

