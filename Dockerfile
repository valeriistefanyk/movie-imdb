FROM python:3.10

# set work directory
WORKDIR /src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
COPY requirements.txt .
RUN apt update && apt install -y gettext && rm -rf /var/apt/cache
RUN pip install --upgrade pip && pip install -r requirements.txt

# copy project
COPY . .

RUN ["chmod", "+x", "./entrypoint.sh"]
RUN ["chmod", "+x", "./manage.py"]

# run entrypoint.sh
ENTRYPOINT [ "/src/entrypoint.sh" ]