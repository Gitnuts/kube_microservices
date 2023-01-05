delete-kubernetes-all:
	kubectl delete deployment --all -n airflow
	kubectl delete statefulset --all -n airflow
	kubectl delete service --all -n airflow
	kubectl delete pod --all -n airflow

deploy-to-gcp:
	make delete-kubernetes-all
	helm upgrade --install -f values.yaml airflow apache-airflow/airflow --namespace airflow --create-namespace --debug
	kubectl apply -f tradingview.yaml -n airflow
	kubectl apply -f zookeeper.yaml -n airflow
	kubectl apply -f kafka.yaml -n airflow
	kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow
