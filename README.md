# Cloud-Computing-Microservice-Architecture

The project's primary objective is to transition a monolithic architecture based e-commerce web application into a microservices architecture.

![image](https://github.com/revanthsreeram/018_036_039_070_Migrating-a-monolithic-e-commerce-application-to-a-microservices-architecture/assets/103492140/1408d136-ed38-4449-91b1-3620430ca780)
the above image shows a monolithic e-commerce application. Consumers access the services through the respective controllers which redirect their requests to the respective services.

![image](https://github.com/revanthsreeram/018_036_039_070_Migrating-a-monolithic-e-commerce-application-to-a-microservices-architecture/assets/103492140/85d9e3b9-c1de-4c00-9fd8-ffbf87c96888)
we direct consumers to access the application through an api gateway.

Meanwhile, we can start developing the microservices.

![image](https://github.com/revanthsreeram/018_036_039_070_Migrating-a-monolithic-e-commerce-application-to-a-microservices-architecture/assets/103492140/3be8294e-1793-49f1-9f13-b69af79cf9cf)
we create a sandbox user and direct all the requests coming from it to the developed microservices through the api gateway. We do this to make sure that the microservices are functioning properly.

![image](https://github.com/revanthsreeram/018_036_039_070_Migrating-a-monolithic-e-commerce-application-to-a-microservices-architecture/assets/103492140/99234db7-9c95-4e3c-9057-2c792f837810)
once we verify the working of the microservices we can redirect all the consumer's requests to the microservices and remove those components from the monolithic application.


# Procedure to run the code:
  1. Run: minikube start
  2. Run the Makefile
  3. Run: minikube service ui-service --url(should open the website in a new tab)

