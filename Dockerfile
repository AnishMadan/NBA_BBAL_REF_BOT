FROM python:3

RUN mkdir nba_bot

COPY . /nba_bot

WORKDIR /nba_bot/

RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD [ "python", "reply_post.py" ] 