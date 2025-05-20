FROM python:3.9-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# When running localy
# CMD ["streamlit", "run", "app.py"]

# When runnning on HuggingFace
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

# docker build -t my-streamlit-app .
# docker run -p 8501:8501 -v "$(pwd)":/app my-streamlit-app