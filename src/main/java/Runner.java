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

public class Runner {
    public static void main(String[] args) {
        BasicConfigurator.configure(NullAppender.getNullAppender());

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
