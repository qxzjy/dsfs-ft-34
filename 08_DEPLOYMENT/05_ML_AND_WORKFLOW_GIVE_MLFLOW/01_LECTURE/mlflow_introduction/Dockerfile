FROM continuumio/miniconda3

WORKDIR /home/app

RUN apt-get update
RUN apt-get install nano unzip
RUN apt install curl -y

RUN curl -fsSL https://get.deta.dev/cli.sh | sh

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install

COPY requirements.txt /dependencies/requirements.txt
RUN pip install -r /dependencies/requirements.txt

ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY
ENV BACKEND_STORE_URI=$BACKEND_STORE_URI
ENV ARTIFACT_STORE_URI=$ARTIFACT_STORE_URI

CMD mlflow server -p $PORT \
    --host 0.0.0.0 \
    --backend-store-uri $BACKEND_STORE_URI \
    --default-artifact-root $ARTIFACT_STORE_URI



# docker build . -t mlflow-server-introduction

# docker run -it\
#  -p 7860:7860\
#  -v "$(pwd):/home/app"\
#  -e MLFLOW_TRACKING_URI="https://qxzjy-mlflow-introduction.hf.space"\
#  mlflow-server-introduction python trainmodel.py