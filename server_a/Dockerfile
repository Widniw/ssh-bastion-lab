FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y openssh-server && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /var/run/sshd

COPY server_a_key.pub /tmp/server_a_key.pub

RUN useradd -s /bin/bash stauto && \
    mkdir -p /home/stauto && \
    mkdir -p /home/stauto/.ssh && \
    cat /tmp/server_a_key.pub >> /home/stauto/.ssh/authorized_keys && \
    chown -R stauto:stauto /home/stauto && \
    chmod 700 /home/stauto/.ssh && \
    chmod 600 /home/stauto/.ssh/authorized_keys && \
    rm /tmp/server_a_key.pub

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]