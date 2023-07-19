FROM python:3.11

WORKDIR /hostd_exporter

COPY requirements.txt ./

RUN pip install -r ./requirements.txt

COPY hostd_exporter.py ./

CMD python hostd_exporter-py