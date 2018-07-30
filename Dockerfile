FROM registry.docker-cn.com/library/python:3.6-slim-jessie
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["try.py"]