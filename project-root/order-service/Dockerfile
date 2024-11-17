# order-service/Dockerfile
FROM maven:3.8.4-openjdk-17 AS builder

WORKDIR /build
COPY pom.xml .
COPY src src

# Package the application
RUN mvn clean package -DskipTests

# Run stage
FROM openjdk:17-jdk-slim
WORKDIR /app
COPY --from=builder /build/target/*.jar app.jar

EXPOSE 8083
ENTRYPOINT ["java", "-jar", "app.jar"]