FROM python:latest

COPY . /app/

RUN pip install -r app/requirements.txt

RUN echo "Cookies and cheesecakes are my favorites" > favorites_cakes.txt

CMD ["python", "/app/app.py"]