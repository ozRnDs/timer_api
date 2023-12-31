FROM python


WORKDIR /usr/src

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./src . 


ENTRYPOINT python main.py
