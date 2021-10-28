# Set  base image (host OS)
FROM python:3.8

#set the workign directory int eh container

WORKDIR /6156-Spring1-Forum

# install dependencies
COPY . .
# RUN pip install -r requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# command to run on container start

EXPOSE 5000

CMD ["python3", "app.py"]