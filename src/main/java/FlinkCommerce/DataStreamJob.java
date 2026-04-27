package FlinkCommerce;

import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;

public class DataStreamJob {
    public static void main(String[] args) throws Exception {
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        String topic = "financial-transactions";

        env.execute("Flink API Skeleton");
    }
}