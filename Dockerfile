# Dockerfile
FROM python:3.9

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV DJANGO_USER=admin2
ENV DJANGO_EMAIL=admin@example.com
ENV DJANGO_PASSWORD=adminadminadmin
# Set the DJANGO_SETTINGS_MODULE environmen
ENV DJANGO_SETTINGS_MODULE=ivrMock.settings

EXPOSE 7000

# Define the entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
