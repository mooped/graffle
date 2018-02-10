.phony: restart logs 

restart:
	gcloud compute instances stop graffle-1
	gcloud compute instances start graffle-1

logs:
	gcloud logging read "resource.type=global AND jsonPayload.instance.name=graffle-1 AND logName=projects/datalogger-194618/logs/gcplogs-docker-driver" --limit 20
