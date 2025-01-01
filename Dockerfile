FROM python:3.9

COPY ./requirements.txt .
COPY ./blueprint ./blueprint
COPY DBConnection.py .
COPY sql_provider.py .

RUN pip install --user -r requirements.txt

CMD ["python", "-m", "blueprint"]