FROM python:3.6
WORKDIR /podcast
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "-m", "podcast"]
