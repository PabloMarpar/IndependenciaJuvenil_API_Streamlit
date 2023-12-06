FROM python:3.11-slim

RUN mkdir /streamlit

COPY config.toml /streamlit/config.toml

COPY requirements.txt /streamlit

WORKDIR /streamlit

RUN pip install -r requirements.txt

COPY . /streamlit

EXPOSE 8501

CMD ["streamlit", "run", "Página de Inicio.py"]
