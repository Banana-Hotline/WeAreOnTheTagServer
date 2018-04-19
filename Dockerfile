FROM python:3.4.8-jessie

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5002

CMD [ "python", "./server.py" ]
