# Cloud Computing: Microservice Architecture

This project is a cloud-based e-commerce application built using a microservices architecture. The application is designed to provide a scalable and fault-tolerant platform for users to browse and purchase products.

## Architecture
The application is composed of the following microservices:

1. Product Service: Responsible for managing product information, including product ID, name, price, quantity, and image URL.
2. Cart Service: Handles user cart operations, including adding, removing, and updating items.
3. Order Service: Manages order processing, including payment processing and order status updates.
4. Auth Service: Handles user authentication and registration.
5. Frontend: A web-based interface for users to interact with the application.

## Requirements
- Python 3.9+
- FastAPI
- MongoDB
- Flask

## Setup Instructions

1. Clone the repository: 
```bash
git clone https://github.com/AditiPrabhuA/AniMerch.git
```

2. Install dependencies: 
```bash
pip install -r requirements.txt
```
3. Start minikube
```bash
minikube start
```

4. Start the services in individual terminals:
```bash
make build-{service_name}
make deploy-{servive_name}
make test-{service_name}
```
5. Run minikube tunnel in a new terminal
```bash
minikube tunnel
```

6. Click on the link provided by the ui service to access the website

### NOTE: replace the mongodb connection uri and the docker hub repository names with actual ones before running
