# CyberGuardAI

### How to start docker
First, make sure you have the docker engine installed.

To build the image, run:
docker build . -t cyberguardai:latest

To start a container of the image:
docker run -d -p 2222:22 cyberguardai:latest

### How to SSH into it
Once the container is running on your local machine, you ssh into it by:

ssh -p 2222 <user>@localhost

where <user> is replaced by i.e. admin (whose password is "admin_password")