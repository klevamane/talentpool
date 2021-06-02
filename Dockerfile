# syntax=docker/dockerfile:1
FROM python:3
# set environment variables
# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
# ie it allows the output to be sent straight to the terminal in real time
ENV PYTHONUNBUFFERED 1
RUN useradd -m talentpooluser
USER talentpooluser
WORKDIR /talentpool
COPY requirements.txt /talentpool/
RUN pip install -r requirements.txt
COPY . /talentpool/
# copy entrypoint.sh
COPY ./entrypoint.sh /talentpool/

# run entrypoint.sh
ENTRYPOINT ["/talentpool/entrypoint.sh"]
