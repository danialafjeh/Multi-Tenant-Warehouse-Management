FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .

#RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt \
    -i https://mirror-pypi.runflare.com/simple/ \
    --trusted-host mirror-pypi.runflare.com

COPY . .

RUN chmod +x entrypoint.sh

EXPOSE 8000

CMD ["./entrypoint.sh"]
