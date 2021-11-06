# Pet Store Docker Image

This image contains the full Pet Store application and all it's dependencies installed. However, for demonstration purposes, we will be only starting one package at a time. The following environment variables can be used for specifying the package to be started and the dependencies it should wait for.

* `WAIT_FOR` - Dependencies to wait for (e.g.:- `tcp://pet-apis:8080`)
* `PET_STORE_PACKAGE` - Pet store package to start up (this should be one of `pet_store`, `pets`)
