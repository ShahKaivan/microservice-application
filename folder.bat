@echo off

:: Set the root directory name
set ROOT_DIR=project-root

:: Create root folder
mkdir %ROOT_DIR%

:: Create files and folders in root
cd %ROOT_DIR%
mkdir auth-service product-service order-service kong
type nul > docker-compose.yml
type nul > .env

:: Create files and folders in auth-service
cd auth-service
type nul > Dockerfile
type nul > main.go
type nul > go.mod
cd ..

:: Create files and folders in product-service
cd product-service
type nul > Dockerfile
type nul > requirements.txt
type nul > main.py
type nul > product_model.py
cd ..

:: Create files and folders in order-service
cd order-service
type nul > Dockerfile
type nul > pom.xml
mkdir src
cd src
mkdir main
cd main
mkdir java
cd java
mkdir com
cd com
mkdir ecommerce
cd ecommerce
type nul > OrderApplication.java
mkdir model
cd model
type nul > Order.java
cd ..
mkdir controller
cd controller
type nul > OrderController.java
cd ..\..\..\..\..\resources
mkdir resources
cd resources
type nul > application.yml
cd ..\..\..\..

:: Create files and folders in kong
cd kong
type nul > kong.yml
cd ..

@echo Directory structure created successfully!
pause
