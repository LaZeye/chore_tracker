FROM python:3.12-slim

WORKDIR /app

RUN useradd -m -u 1000 mark

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir pymongo==4.8.0

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

USER mark

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--debug"]