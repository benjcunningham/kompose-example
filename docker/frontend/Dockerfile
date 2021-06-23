FROM python:3.9
WORKDIR /frontend
COPY frontend/requirements.txt .
RUN pip install -r requirements.txt
COPY frontend/ .
EXPOSE 80
CMD ["streamlit", "run", "main.py", "--server.port", "80"]
