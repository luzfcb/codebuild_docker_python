FROM python:3.7



ENV        PYTHONUNBUFFERED 1

RUN set -ex \
    && echo 'Acquire::CompressionTypes::Order:: "gz";' > /etc/apt/apt.conf.d/99use-gzip-compression \
    && apt-get update \
    && apt-get install -y apt-transport-https \
    && apt-get install -y \
       graphviz \
       && rm -rf /var/lib/apt/lists/* \
    && apt-get clean




RUN        mkdir -p /var/project/app
WORKDIR    /var/project/app/

COPY       manage.py /var/project/app/
COPY       requirements/ /var/project/app/requirements
RUN        pip install -r /var/project/app/requirements/production.txt --no-cache-dir

COPY       foobar_proj /var/project/app/foobar_proj

EXPOSE     8081
CMD        ["/var/app/run_local.sh"]
