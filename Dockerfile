# alpine is a smaller version
FROM python:3.7-alpine
# instead of maintainer tag listed with inspect
LABEL maintainer="pawlo97.pb@gmail.com"
# Recommended when running python in a container
# Doesn't allow to buffer output
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# install stuff for psycopg2 no cache is for minimizing #of deps installed
RUN apk add --update --no-cache postgresql-client jpeg-dev
# stuff needed before running requirements and not needed after
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

# copy app files and set workdir
RUN mkdir /app
WORKDIR /app
COPY ./app /app

# now you know what to share with nginX
# -p means create all stuff on the way vol and web here before media
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static
# add user that can run stuff
# used for security as by default root is used
RUN adduser -D user
# set permissions for all folders inside vol
RUN chown -R user:user /vol/
RUN chmod -R 755 /vol/web
# change curr user
USER user

