FROM python:latest
LABEL author=23skdu@users.noreply.github.com
RUN apt update && apt -y upgrade \
    && pip3 install python-lsp-server streamlit numpy pandas matplotlib tensorflow scikit-learn plotly
COPY tool /bin
CMD ["python","-c", "print('works')"] 
