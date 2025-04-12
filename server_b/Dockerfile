FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y openssh-server vim && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/sshd

COPY server_b_key.pub /tmp/server_b_key.pub

RUN useradd -s /bin/bash stauto && \
    mkdir -p /home/stauto && \
    mkdir -p /home/stauto/.ssh && \
    cat /tmp/server_b_key.pub >> /home/stauto/.ssh/authorized_keys && \
    chown -R stauto:stauto /home/stauto && \
    chmod 700 /home/stauto/.ssh && \
    chmod 600 /home/stauto/.ssh/authorized_keys && \
    rm /tmp/server_b_key.pub

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]