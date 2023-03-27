FROM python:3.11.2

WORKDIR /APP

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "main.py"]

EXPOSE 80/tcp
EXPOSE 443/tcp
EXPOSE 5222/tcp
