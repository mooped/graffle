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
