FROM python:3.8
WORKDIR /app
RUN pip install streamlit Flask

COPY src/app.py /app/
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]

