# Pet Store Sample

A sample Pet Store application.

## Requirements

* Docker
* Docker Compose

## Starting Up Pet Store without Log Collection

1. Clone and navigate to the root of this repository.
2. Startup the docker compose setup.
   ```bash
   docker-compose pull
   docker-compose up --force-recreate --renew-anon-volumes --no-build
   ```
3. Go to http://localhost:8080/docs to view the OAS spec for the API and invoke using the available UI.

## Starting Up Pet Store with Log Collection

1. Clone and navigate to the root of this repository.
2. Startup the docker compose setup.
   ```bash
   docker-compose pull
   docker-compose -f ./log-collection/docker-compose-collector.yaml up --force-recreate --renew-anon-volumes
   docker-compose -f docker-compose.yaml -f log-collection/docker-compose-pet-store-override.yaml up --build --force-recreate --renew-anon-volumes
   ```
3. Go to http://localhost:8080/docs to view the OAS spec for the API and invoke using the available UI.
4. Go to http://localhost:5601 to view the Kibana dashboard.

## Cleaning Up

Run the following command to cleanup all created resources

```bash
docker-compose down
```
