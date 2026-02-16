FROM python:3.9-slim
WORKDIR /app
RUN pip install --no-cache-dir flask requests
COPY . .
# Logların terminalde anlık görünmesi için 'unbuffered' modu
ENV PYTHONUNBUFFERED=1
CMD ["python", "server_api.py"]