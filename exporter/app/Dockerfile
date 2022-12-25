FROM python:3.8-alpine

ENV APP_HOME=/app
ENV APP_PORT=9877

RUN mkdir $APP_HOME

WORKDIR $APP_HOME

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py $APP_HOME

EXPOSE $APP_PORT

HEALTHCHECK --interval=60s --timeout=12s CMD python -c "import requests; requests.get('http://localhost:${APP_PORT}', timeout=2)"

CMD [ "python3", "app.py" ]