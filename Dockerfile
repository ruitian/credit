FROM python:2.7
RUN mkdir -p /credit
WORKDIR /credit
COPY . /credit
ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD ['python', 'manage.py', 'runserver']
EXPOSE 3000
