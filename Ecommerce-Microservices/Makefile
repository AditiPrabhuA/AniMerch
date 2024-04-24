# Makefile
IMAGE_NAME=aditiprabhu/ecommerce
IMAGE_TAG=v9
IMAGE_NAMEp=aditiprabhu/ecommercep
IMAGE_TAGp=v2
IMAGE_NAMEu=aditiprabhu/ecommerceu
IMAGE_TAGu=v3
build-order:
	docker build -t $(IMAGE_NAME):$(IMAGE_TAG) ./Order
	docker push $(IMAGE_NAME):$(IMAGE_TAG)

deploy-order:
	kubectl apply -f Order/orderapp.yaml
	kubectl apply -f Order/orderapp-svc.yaml
	kubectl set image deployment/orderapp orderapp=$(IMAGE_NAME):$(IMAGE_TAG)

build-product:
	docker build -t $(IMAGE_NAMEp):$(IMAGE_TAGp) ./Product
	docker push $(IMAGE_NAMEp):$(IMAGE_TAGp)

deploy-product:
	kubectl apply -f Product/productapp.yaml
	kubectl apply -f Product/productapp-svc.yaml
	kubectl set image deployment/productapp productapp=$(IMAGE_NAMEp):$(IMAGE_TAGp)

build-user:
	docker build -t $(IMAGE_NAMEu):$(IMAGE_TAGu) ./User
	docker push $(IMAGE_NAMEu):$(IMAGE_TAGu)

deploy-user:
	kubectl apply -f User/userapp.yaml
	kubectl apply -f User/userapp-svc.yaml
	kubectl set image deployment/userapp userapp=$(IMAGE_NAMEu):$(IMAGE_TAGu)

run-frontend:
	cd frontend && set FLASK_APP=app.py && flask run

test-order:
	minikube service orderapp-svc --url

test-product:
	minikube service productapp-svc --url

test-user:
	minikube service userapp-svc --url