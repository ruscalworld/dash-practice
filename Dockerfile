FROM python:3.13-slim

WORKDIR /home/practice
ADD . .
RUN pip3 install -r requirements.txt

ENV ENVIRONMENT=production
CMD ["python", "main.py"]
