FROM python:3.8
RUN apt update && apt install poppler-utils -y
COPY setup.py setup.cfg README.rst ./
COPY refextract refextract/
RUN python setup.py install 
ENTRYPOINT exec gunicorn -b :5000 --access-logfile - --error-logfile - refextract.app:app --timeout 650
