import com.codahale.metrics.MetricRegistry;
import com.codahale.metrics.Timer;
import java.util.Random;
import static com.codahale.metrics.MetricRegistry.name;

public class Worker implements Runnable {
    private final MetricRegistry metricRegistry;

    public Worker(MetricRegistry metricRegistry) {
        this.metricRegistry = metricRegistry;
        metricRegistry.counter(name(Worker.class, "worker-amounts")).inc();
    }

    public void run() {
        Random random = new Random();
        Timer timer = metricRegistry.timer(name(Worker.class, "processing-time"));


        Timer.Context context = null;
        try {
            while (!Thread.interrupted()) {
                context = timer.time();
                Thread.sleep(random.nextInt(1000));
                context.stop();
            }
        } catch (InterruptedException e) {
            System.out.println("interrupted in sleep: " + this);
        } finally {
            Thread.currentThread().interrupt();
            metricRegistry.counter(name(Worker.class, "worker-amounts")).dec();
            context.stop();
        }
    }

}
