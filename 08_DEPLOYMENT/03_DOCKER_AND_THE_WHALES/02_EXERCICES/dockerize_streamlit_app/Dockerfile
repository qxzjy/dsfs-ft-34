FROM python:latest

COPY . /app/

RUN pip install -r app/requirements.txt

CMD ["streamlit", "run", "--server.port", "4000", "--server.address", "0.0.0.0", "app/app.py"]

# docker run -it -v "$(pwd):/home/app" -p 4000:4000 dockerize_streamlit_app