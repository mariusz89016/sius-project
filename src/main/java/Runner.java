import com.codahale.metrics.Gauge;
import com.codahale.metrics.MetricRegistry;
import com.github.jjagged.metrics.reporting.StatsDReporter;
import com.netflix.dyno.connectionpool.Host;
import com.netflix.dyno.connectionpool.HostSupplier;
import com.netflix.dyno.connectionpool.TokenMapSupplier;
import com.netflix.dyno.connectionpool.impl.ConnectionPoolConfigurationImpl;
import com.netflix.dyno.connectionpool.impl.lb.HostToken;
import com.netflix.dyno.jedis.DynoJedisClient;
import org.apache.log4j.BasicConfigurator;
import org.apache.log4j.varia.NullAppender;

import java.util.Collections;
import java.util.List;
import java.util.Set;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;

import static com.codahale.metrics.MetricRegistry.name;

public class Runner {
    static final MetricRegistry metrics = new MetricRegistry();

    public static void main(String[] args) throws InterruptedException {
        BasicConfigurator.configure(NullAppender.getNullAppender());

        testStatsDReporting();
        testDynomite();
    }


    private static void testStatsDReporting() throws InterruptedException {
        StatsDReporter statsDReporter = StatsDReporter.forRegistry(metrics)
                .prefixedWith("workers-test3")
                .build("172.18.0.4", 8125);
        statsDReporter.start(1, TimeUnit.MILLISECONDS);
        final ThreadPoolExecutor threadPoolExecutor = (ThreadPoolExecutor) Executors.newCachedThreadPool();
//        threadPoolExecutor.setCorePoolSize(50);

        metrics.register(name(Runner.class, "executor-size"), new Gauge<Integer>() {
            public Integer getValue() {
                return threadPoolExecutor.getPoolSize();
            }
        });

        for (int i = 0; i < 100; i++) {
            threadPoolExecutor.execute(new Worker(metrics));
        }

        System.out.println("before sleep");
        Thread.sleep(3000);
        System.out.println("after sleep");

        for (int i = 0; i < 100; i++) {
            threadPoolExecutor.execute(new Worker(metrics));
            Thread.sleep(200);
        }
        System.out.println("shutdown");
        threadPoolExecutor.shutdownNow();
        System.out.println(threadPoolExecutor.awaitTermination(10, TimeUnit.SECONDS));
        System.out.println(threadPoolExecutor.getActiveCount());
    }

    private static void testDynomite() {
        final int port = 8102;
        final Host localHost = new Host("172.18.0.2", port, Host.Status.Up);
        final HostSupplier localHostSupplier = () -> Collections.singletonList(localHost);

        final TokenMapSupplier supplier = new TokenMapSupplier() {
            @Override
            public List<HostToken> getTokens(Set<Host> activeHosts) {
                return Collections.singletonList(localHostToken);
            }

            @Override
            public HostToken getTokenForHost(Host host, Set<Host> activeHosts) {
                return localHostToken;
            }

            final HostToken localHostToken = new HostToken(100000L, localHost);
        };

        DynoJedisClient jedisClient = new DynoJedisClient.Builder()
                .withApplicationName("tokenSupplierExample")
                .withDynomiteClusterName("tokenSupplierExample")
                .withHostSupplier(localHostSupplier)
                .withCPConfig(new ConnectionPoolConfigurationImpl("tokenSupplierExample")
                        .withTokenSupplier(supplier).setConnectTimeout(10000))
                .withPort(port)
                .build();

        jedisClient.set("foo", "puneetTest");
        System.out.println("Value: " + jedisClient.get("foo"));
        jedisClient.stopClient();
    }
}
