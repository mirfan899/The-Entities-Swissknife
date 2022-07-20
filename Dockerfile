FROM python:3.9.7-bullseye

WORKDIR app/

COPY . .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt

EXPOSE 8501
CMD ["streamlit", "run", "main.py"]