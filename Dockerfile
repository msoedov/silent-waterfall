FROM python:3.6

WORKDIR /app

COPY pip.txt ./
RUN pip install --no-cache-dir -r pip.txt
COPY . .
CMD [ "python", "-u", "app.py" ]
