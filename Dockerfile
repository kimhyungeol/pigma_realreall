# ./Dockerfile
FROM python:3.8.9
WORKDIR /app

## Install packages
COPY requirements.txt ./
RUN python -m pip install --upgrade pip --user
RUN pip3 install -r requirements.txt


## Copy all src files
COPY . .

## Run the application on the port 8000
EXPOSE 8000

# gunicorn 배포 명령어
# CMD ["gunicorn", "--bind", "허용하는 IP:열어줄 포트", "project.wsgi:application"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]