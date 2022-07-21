FROM debian
FROM python

WORKDIR /app

COPY index.py .

RUN python -m pip install pyyaml

ENTRYPOINT [ "python", "index.py" ]