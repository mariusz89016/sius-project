package pl.edu.agh.hystrix.command;

import com.netflix.hystrix.HystrixCommand;
import com.netflix.hystrix.HystrixCommandGroupKey;

import java.util.Random;

/**
 * Created by krzys on 19.05.16.
 */
public class HelloWorldCommand extends HystrixCommand<String> {
    private final String name;

    public HelloWorldCommand(String name) {
        super(HystrixCommandGroupKey.Factory.asKey("ExampleGroup"));
        this.name = name;
    }

    @Override
    protected String run() {
        if (new Random().nextFloat() < 0.4) {
            throw new RuntimeException();
        }
        return "Hello " + name + "!";
    }
}
