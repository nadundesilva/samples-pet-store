# Pet Store Sample

A sample Pet Store application.

## Requirements

* Docker
* Docker Compose

## Starting Up

1. Startup the docker compose setup
   ```bash
   VERSION=latest docker-compose pull
   VERSION=latest docker-compose up --no-build --force-recreate --renew-anon-volumes
   ```
2. Go to http://localhost:8080/docs to view the OAS spec for the API and invoke using the available UI.

## Cleaning Up

Run the following command to cleanup all created resources

```bash
docker-compose down
```
