
FROM python:3.9


WORKDIR /src


COPY ./src/requirements.txt /src/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
ENV API_TEST=0

COPY ./src /src

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host=0.0.0.0","--reload"]
