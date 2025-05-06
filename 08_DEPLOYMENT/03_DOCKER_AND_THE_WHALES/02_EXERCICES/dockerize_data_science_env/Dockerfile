FROM python:latest

COPY requirements.txt .

RUN pip install -r requirements.txt

WORKDIR /notebooks

CMD ["jupyter", "lab", "--ip=*", "--port=8888", "--allow-root", "--no-browser"]

# docker run -v "$(pwd):/notebooks" -p 8888:8888  data_science_env