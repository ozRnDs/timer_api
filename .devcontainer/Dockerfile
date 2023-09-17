FROM python


RUN mkdir /usr/src

WORKDIR /usr/src

COPY ../requirements.txt ../requirements-dev.txt ./

RUN pip install -r requirements.txt

# COPY src /usr/src

# ENTRYPOINT python main.py
