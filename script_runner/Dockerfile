FROM python:3.13-bookworm

COPY requirements.txt /rem_device_stat_check/requirements.txt

RUN apt-get update && apt-get install -y \
    openssh-client iputils-ping vim && \
    pip install -r /rem_device_stat_check/requirements.txt

CMD ["python3", "/rem_device_stat_check/main.py", "-t", "30"]