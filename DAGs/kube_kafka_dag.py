from datetime import timedelta, datetime
import os
import airflow
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from kubernetes.client import models as k8s
from airflow.providers.google.cloud.operators.kubernetes_engine import GKEStartPodOperator


EXECUTION_DATE = '{{ execution_date }}'


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(0, hour=0, minute=0, second=0),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'wait_for_downstream': False,
}


with DAG(
    dag_id='kafka_prod',
    default_args=default_args,
    description='Kafka producer',
    schedule_interval="29,59 * * * *",
    max_active_runs=1,
    catchup=False,
) as dag:

    kubernetes_pod = GKEStartPodOperator(
        task_id="kafka_consumer",
        name="Kafka_consumer",
        project_id="###",  # name of project in GCP
        location="###",  # location of GKE, e.g us-west4-b
        cluster_name="automato-cluster",  # name of GKE cluster
        namespace="airflow",
        image_pull_policy="Always",
        image_pull_secrets=[k8s.V1LocalObjectReference('secret')],  # set an image pull secret in GKE
        image="###",  # path to docker image in GCP
        get_logs=True,
        is_delete_operator_pod=True,
    )

    producer = BashOperator(
        task_id='kafka_producer',
        bash_command='pod_name=$(kubectl get pods -n airflow -o custom-columns=":metadata.name" | \
        grep api-tradingview) && \
        kubectl exec -n airflow -it "$pod_name" -- bash -c "bash exec.sh"',
    )
    
