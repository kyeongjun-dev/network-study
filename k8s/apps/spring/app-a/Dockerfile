FROM amazoncorretto:17

WORKDIR /app

COPY . .
RUN ./gradlew build -x test

RUN cp /app/build/libs/*.jar /app/app.jar
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
# port 8080