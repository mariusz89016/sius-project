package pl.edu.agh.hystrix;

import pl.edu.agh.hystrix.command.HelloWorldCommand;
import spark.Request;
import spark.Response;
import spark.Route;
import spark.Spark;
import spark.servlet.SparkApplication;

public class HelloWorld implements SparkApplication {
    @Override
    public void init() {
        Spark.get("/hello", new Route() {
            @Override
            public Object handle(Request request, Response response) {
                return new HelloWorldCommand(request.queryParams("name")).execute();
            }
        });
    }
}
