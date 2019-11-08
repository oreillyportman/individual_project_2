FROM python:2.7
WORKDIR /app
RUN pip install gunicorn
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# ENTRYPOINT ["/usr/local/bin/gunicorn", "-b", "0.0.0.0:5000", "application.__init__:app"]
ENTRYPOINT ["python", "run.py"]
