IMAGE_NAME={docker_hub_repository}
IMAGE_TAG=auth21
build-auth:
	docker build --no-cache -t $(IMAGE_NAME):$(IMAGE_TAG) ./backend/auth
	docker push $(IMAGE_NAME):$(IMAGE_TAG)

deploy-auth:
	kubectl apply -f backend/auth/auth-deployment.yaml
	kubectl apply -f backend/auth/auth-service.yaml
	kubectl set image deployment/auth auth=$(IMAGE_NAME):$(IMAGE_TAG)

test-auth:
	minikube service auth-service --url

IMAGE_NAME2={docker_hub_repository}
IMAGE_TAG2=ui33
build-ui:
	docker build --no-cache -t $(IMAGE_NAME2):$(IMAGE_TAG2) ./frontend
	docker push $(IMAGE_NAME2):$(IMAGE_TAG2)

deploy-ui:
	kubectl apply -f frontend/ui-deployment.yaml
	kubectl apply -f frontend/ui-service.yaml
	kubectl set image deployment/ui ui=$(IMAGE_NAME2):$(IMAGE_TAG2)

test-ui:
	minikube service ui-service --url

IMAGE_NAME3={docker_hub_repository}
IMAGE_TAG3=cart38
build-cart:
	docker build --no-cache -t $(IMAGE_NAME3):$(IMAGE_TAG3) ./backend/cart
	docker push $(IMAGE_NAME3):$(IMAGE_TAG3)

deploy-cart:
	kubectl apply -f backend/cart/cartapp.yaml
	kubectl apply -f backend/cart/cartapp-svc.yaml
	kubectl set image deployment/cartapp cartapp=$(IMAGE_NAME3):$(IMAGE_TAG3)

test-cart:
	minikube service cartapp-svc --url

IMAGE_NAME4={docker_hub_repository}
IMAGE_TAG4=prod23
build-product:
	docker build --no-cache -t $(IMAGE_NAME4):$(IMAGE_TAG4) ./backend/product
	docker push $(IMAGE_NAME4):$(IMAGE_TAG4)

deploy-product:
	kubectl apply -f backend/product/product-deployment.yaml
	kubectl apply -f backend/product/product-service.yaml
	kubectl set image deployment/product product=$(IMAGE_NAME4):$(IMAGE_TAG4)

test-product:
	minikube service product-service --url

