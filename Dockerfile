FROM python:3.10.10
WORKDIR ./scanner
COPY requirements.txt .
COPY ./src ./src
RUN pip install -r requirements.txt
EXPOSE 8084/tcp
ENV PORT=8084
ENV HOST=127.0.0.1
ENV CONTROLLER_HOST=10.0.0.183
ENV CONTROLLER_PORT=8082
ENV NAME=testScanner
CMD ["python", "src/main.py"]