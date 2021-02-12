FROM python:3.8-slim-buster

WORKDIR /gets_app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "-m", "voila", "Interface_temporal_GETS.ipynb", "--host=0.0.0.0"]