FROM debian:latest

RUN apt-get update && apt-get install -y openssh-server
RUN mkdir /var/run/sshd
RUN echo 'root:root123' | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config

RUN useradd -m -s /bin/bash admin
RUN echo "admin:admin_password" | chpasswd

RUN useradd -m -s /bin/bash oscpal
RUN echo "oscpal:oscpal_password" | chpasswd

EXPOSE 22

CMD ["/usr/sbin/sshd", "-D"]