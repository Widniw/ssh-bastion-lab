FROM python:3.13-bookworm

COPY requirements.txt /rem-device-stat-check/requirements.txt

RUN apt-get update && apt-get install -y \
    openssh-client iputils-ping && \
    pip install -r /rem-device-stat-check/requirements.txt

CMD ["python3", "rem-device-stat-check/main.py"]