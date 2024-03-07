FROM python:3.11-alpine
LABEL author=23skdu@users.noreply.github.com
RUN set +x && apt update && apt -y upgrade \
    && pip3 install argparse requests newrelic prometheus-client opentelemetry-distro \
    && pip3 cache purge
COPY nrsak.py /bin
CMD ["python3","-c","print('works')"] 
