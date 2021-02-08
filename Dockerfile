# alpine is a smaller version
FROM python:3.7-alpine
# instead of maintainer tag listed with inspect
LABEL maintainer="pawlo97.pb@gmail.com"
# Recommended when running python in a container
# Doesn't allow to buffer output
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# copy app files and set workdir
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# add user that can run stuff
# used for security as by default root is used
RUN adduser -D user
USER user

