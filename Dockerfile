FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# Install python3 and dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get install -y python3.12 curl && \
    apt-get install wkhtmltopdf -y && \
    curl -sS https://bootstrap.pypa.io/get-pip.py | python3.12 && \
    mv /usr/bin/wkhtmltopdf /usr/local/bin/. && \
    rm -rf /var/lib/apt/lists/* /root/.cache /tmp/*

RUN curl -sSL https://install.python-poetry.org | python3.12 - --preview

RUN pip3 install --upgrade requests

# Python 3.12 default version
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.12 1 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1

# Upgrade pip
RUN python3 -m pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN pip install --upgrade six

# Remove cache pip
RUN pip cache purge

COPY ./app /code/

# CMD ["fastapi", "run", "app/main.py", "--port", "8000", "--reload"]