FROM python:3.8.6-slim
WORKDIR /app

COPY [".", "/app"]
RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["flask", "run", "--host", "0.0.0.0"] 