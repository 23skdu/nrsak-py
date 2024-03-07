FROM python:latest
LABEL author=23skdu@users.noreply.github.com
RUN set +x && apt update && apt -y upgrade \
    && pip3 install python-lsp-server newrelic prometheus-client opentelemetry-distro numpy pandas matplotlib tensorflow scikit-learn plotly re requests 
COPY nrsak.py /bin
CMD ["python","-c", "print('works')"] 
