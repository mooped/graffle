.phony: up console

up:
	docker-compose up --build -d

console:
	docker-compose up --build

push: up
	docker tag graffle_graffle us.gcr.io/datalogger-194618/graffle/graffle
	gcloud docker -- push us.gcr.io/datalogger-194618/graffle/graffle
	gcloud compute instances stop graffle-1
	gcloud compute instances start graffle-1

logs:
	gcloud logging read "resource.type=global AND jsonPayload.instance.name=graffle-1 AND logName=projects/datalogger-194618/logs/gcplogs-docker-driver" --limit 20
