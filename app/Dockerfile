FROM python:3

ENV WAIT_VERSION 2.7.2
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ADD sayhello /sayhello
RUN chmod +x /sayhello
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

CMD [ "python3", "./insert.py" ]

