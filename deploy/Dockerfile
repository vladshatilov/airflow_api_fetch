FROM apache/airflow:2.4.2-python3.10
USER root
RUN apt-get update && apt install -y python3-pip python3-psycopg2 \
  && echo "airflow ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
  && echo "root ALL=NOPASSWD: ALL" >> /etc/sudoers
USER airflow
RUN export AIRFLOW_HOME=/opt/airflow
RUN set -ex
RUN pip install --user psycopg2-binary
COPY ./deploy/airflow.cfg /opt/airflow/airflow.cfg

USER airflow
COPY ./deploy/users.sh .
COPY ./deploy/connections.sh .
COPY ./deploy/connections.py .
COPY ./deploy/connections.yaml .

USER root
RUN chmod +x ./users.sh
RUN chmod +x ./connections.sh
RUN chown -R airflow ${AIRFLOW_HOME}

USER airflow

COPY ./src/. /opt/airflow/src/.