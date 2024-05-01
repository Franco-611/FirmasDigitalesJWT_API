
FROM postgres:latest

ENV POSTGRES_DB=FirmasDigitalesJWT
ENV POSTGRES_USER=auth
ENV POSTGRES_PASSWORD=prueba

COPY ./migrations /docker-entrypoint-initdb.d/