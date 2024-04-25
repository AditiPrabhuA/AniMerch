# Makefile
IMAGE_NAME=revanthsreeram/my-merch-microservices-app
IMAGE_TAG=auth4
build-auth:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) ./backend/auth
	docker push $(IMAGE_NAME):$(IMAGE_TAG)

deploy-auth:
	kubectl apply -f backend/auth/auth-deployment.yaml
	kubectl apply -f backend/auth/auth-service.yaml
	kubectl set image deployment/auth auth=$(IMAGE_NAME):$(IMAGE_TAG)

test-auth:
	minikube service auth-service --url

IMAGE_NAME2=revanthsreeram/my-merch-microservices-app
IMAGE_TAG2=ui8
build-ui:
	docker build -t $(IMAGE_NAME2):$(IMAGE_TAG2) ./frontend
	docker push $(IMAGE_NAME2):$(IMAGE_TAG2)

deploy-ui:
	kubectl apply -f frontend/ui-deployment.yaml
	kubectl apply -f frontend/ui-service.yaml
	kubectl set image deployment/ui ui=$(IMAGE_NAME2):$(IMAGE_TAG2)

test-ui:
	minikube service ui-service --url