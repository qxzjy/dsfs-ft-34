FROM python:3.9.9-alpine

WORKDIR /home/app

# Here we set up environment variables according to values that 
# will be passed to the container via the docker run command!
ENV ENV_1=$ENV_1
ENV ENV_2=$ENV_2

RUN echo "Cookies and cheesecakes are my favorites" > favorites_cakes.txt

COPY app.py app.py