# Pet Store Sample

[![Build](https://github.com/nadundesilva/samples-pet-store/workflows/Build%20Branch/badge.svg)](https://github.com/nadundesilva/samples-pet-store/actions/workflows/build-branch.yaml)

A sample Pet Store application.

## Requirements

* Docker
* Docker Compose

## Pet Store without Log Collection

### Starting Up

1. Clone and navigate to the root of this repository.
2. Pull all the required images.
   ```bash
   docker-compose pull
   ```
3. Startup the docker compose setup.
   ```bash
   docker-compose up --force-recreate --renew-anon-volumes --no-build
   ```
4. Go to http://localhost:8080/docs to view the OAS spec for the API and invoke using the available UI.

## Pet Store with Log Collection

### Starting Up

1. Clone and navigate to the root of this repository.
2. Pull all the required images for log collection setup.
   ```bash
   docker-compose -f ./log-collection/docker-compose-collector.yaml pull
   ```
3. Startup the log collection docker compose setup and wait for it to complete startup.
   ```bash
   docker-compose -f ./log-collection/docker-compose-collector.yaml up --force-recreate --renew-anon-volumes
   ```
4. Pull all the required images for services.
   ```bash
   docker-compose -f docker-compose.yaml -f log-collection/docker-compose-pet-store-override.yaml pull
   ```
5. Startup the pet-store with log publishing enabled.
   ```bash
   docker-compose -f docker-compose.yaml -f log-collection/docker-compose-pet-store-override.yaml up --force-recreate --renew-anon-volumes
   ```
6. Go to http://localhost:8080/docs to view the OAS spec for the API and invoke using the available UI.
7. Go to http://localhost:5601 to view the Kibana dashboard.
