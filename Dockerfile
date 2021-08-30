FROM python:3.9

RUN mkdir -p /opt/app
RUN mkdir -p /opt/app/customer
COPY requirements.txt start.sh /opt/app/
COPY app_customer /opt/app/customer/
WORKDIR /opt/app
RUN pip install -r requirements.txt
RUN pip install gunicorn
RUN chown -R www-data:www-data /opt/app
