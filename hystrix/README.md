# Hystrix demo project
`hystrix-hello-world` contains basic hello world application with Hystrix support

## Running example
```
cd hystrix-hello-world
mvn jetty:run
```
Will start local server with demo application on port 8080. You can make a request for `localhost:8080/hello`. It has ~40% chance to return `500 Internal Error` and ~40% chance to return correct response.

# Hystrix dashboard
I've included a standalone version on Hystrix dashboard. To start:
```
java -jar standalone-hystrix-dashboard-1.5.2-all.jar
```
In browser go to http://localhost:7979/hystrix-dashboard/

Add stream to monitor (example for hello-world: http://localhost:8080/hystrix.stream). Click
`Add stream` and `Monitor streams` to see dashboard.

More info https://github.com/kennedyoliveira/standalone-hystrix-dashboard

## Hystrix dashboard docker
See: https://github.com/mlabouardy/hystrix-dashboard-docker

# Running Hystrix examples
```
$ git clone git@github.com:Netflix/Hystrix.git
$ cd Hystrix/hystrix-examples-webapp
$ ../gradlew jettyRun
```
