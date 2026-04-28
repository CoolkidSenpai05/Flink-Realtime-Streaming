# Flink Real-time E-commerce Streaming Analytics

A real-time streaming analytics platform for e-commerce transactions using Apache Flink, Kafka, and PostgreSQL. This project demonstrates building scalable event-driven architectures for processing large volumes of transaction data in real-time.

## 🎯 Project Overview

This application processes e-commerce sales transactions in real-time to generate actionable insights such as:
- **Sales per category** - Track revenue by product category
- **Daily sales metrics** - Monitor sales trends on a daily basis
- **Monthly sales analysis** - Understand long-term sales patterns
- **Real-time transaction storage** - Persist all transactions for analytics

## 🏗️ Architecture

```
┌─────────────────────────┐
│  Sales Transaction      │
│  Generator (Python)     │
└────────────┬────────────┘
             │ (generates fake data)
             ▼
┌─────────────────────────┐
│  Apache Kafka           │
│  financial-transactions │
└────────────┬────────────┘
             │ (streams events)
             ▼
┌─────────────────────────┐
│  Apache Flink           │
│  DataStreamJob          │
└────────────┬────────────┘
             │ (processes, aggregates)
      ┌──────┴──────────┬─────────────┐
      ▼                 ▼             ▼
  PostgreSQL       PostgreSQL    Elasticsearch
  (transactions)   (analytics)   (indexing)
```

## 🛠️ Tech Stack

- **Apache Flink** (1.18.0) - Stream processing engine
- **Apache Kafka** (7.4.0) - Message broker
- **PostgreSQL** - Relational database for persistence
- **Elasticsearch** (7.x) - Full-text search and analytics
- **Java** (1.8) - Backend processing
- **Python** - Data generation
- **Docker & Docker Compose** - Containerization

## 📋 Prerequisites

- Docker and Docker Compose
- Java 8 or higher
- Python 3.7+
- Maven 3.6+
- Git

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/CoolkidSenpai05/Flink-Realtime-Streaming.git
```

### 2. Start Infrastructure Services

Start all required services (Kafka, PostgreSQL, Elasticsearch) using Docker Compose:

```bash
docker-compose up -d
```

This will start:
- **Zookeeper** (port 2181)
- **Kafka** (port 9092)
- **PostgreSQL** (port 5432)
- **Elasticsearch** (port 9200)

Wait for all services to be healthy:

```bash
docker-compose ps
```

### 3. Build the Flink Job

```bash
mvn clean package
```

### 4. Setup Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Linux/Mac:
source venv/bin/activate

# Install dependencies
cd SalesTransactionGenerator
pip install -r requirements.txt
```

### 5. Run the Transaction Generator

In a new terminal, start generating synthetic transaction data:

```bash
cd SalesTransactionGenerator
python main.py
```

This will generate random e-commerce transactions and publish them to Kafka for 2 minutes.

### 6. Submit the Flink Job

```bash
flink run -c FlinkCommerce.DataStreamJob target/FlinkCommerce-1.0-SNAPSHOT.jar
```

Alternatively, use the Flink Web UI:

1. Access Flink Web UI at http://localhost:8081
2. Upload the JAR file: `target/FlinkCommerce-1.0-SNAPSHOT.jar`
3. Click "Submit" and select the main class `FlinkCommerce.DataStreamJob`

## 📁 Project Structure

```
flink-ecommerce/
├── src/
│   └── main/
│       ├── java/
│       │   ├── Deserializer/
│       │   │   └── JSONValueDeserializationSchema.java    # Kafka JSON deserializer
│       │   ├── Dto/
│       │   │   ├── Transaction.java                       # Transaction data model
│       │   │   ├── SalesPerCategory.java                  # Category aggregation DTO
│       │   │   ├── SalesPerDay.java                       # Daily aggregation DTO
│       │   │   └── SalesPerMonth.java                     # Monthly aggregation DTO
│       │   ├── FlinkCommerce/
│       │   │   └── DataStreamJob.java                     # Main Flink streaming job
│       │   ├── utils/
│       │   │   └── JsonUtil.java                          # JSON utility functions
│       │   └── resources/
│       │       └── log4j2.properties                       # Logging configuration
├── SalesTransactionGenerator/
│   ├── main.py                                             # Data generation script
│   └── requirements.txt                                    # Python dependencies
├── docker-compose.yml                                      # Infrastructure setup
├── pom.xml                                                 # Maven configuration
└── README.md                                               # This file
```

## 🔧 Key Components

### DataStreamJob
The main Flink streaming job that:
1. Consumes transactions from Kafka topic `financial-transactions`
2. Deserializes JSON messages into `Transaction` objects
3. Creates and populates three main tables:
   - `transactions` - Raw transaction records
   - `sales_per_category` - Aggregated sales by product category
   - `sales_per_day` - Daily sales metrics
   - `sales_per_month` - Monthly sales metrics
4. Persists data to PostgreSQL using JDBC sink
5. Indexes data in Elasticsearch for full-text search

### Transaction Schema
Each transaction contains:
- Transaction ID (UUID)
- Product ID, Name, Category, Price, Brand, Quantity
- Customer ID
- Total Amount
- Currency
- Payment Method
- Transaction Date/Time

### SalesTransactionGenerator
Generates synthetic e-commerce transaction data using:
- Faker library for realistic customer data
- Random selection for products, categories, brands
- Configurable price ranges and quantities
- Produces to Kafka for 2-minute duration (configurable)

## 🗄️ Database Schema

### Transactions Table
```sql
CREATE TABLE transactions (
    transaction_id VARCHAR(255) PRIMARY KEY,
    product_id VARCHAR(255),
    product_name VARCHAR(255),
    product_category VARCHAR(255),
    product_price DOUBLE PRECISION,
    product_quantity INTEGER,
    product_brand VARCHAR(255),
    total_amount DOUBLE PRECISION,
    currency VARCHAR(255),
    customer_id VARCHAR(255),
    transaction_date TIMESTAMP,
    payment_method VARCHAR(255)
);
```

### Sales Per Category Table
```sql
CREATE TABLE sales_per_category (
    transaction_date DATE,
    category VARCHAR(255),
    total_sales DOUBLE PRECISION,
    PRIMARY KEY (transaction_date, category)
);
```

### Sales Per Day Table
```sql
CREATE TABLE sales_per_day (
    transaction_date DATE PRIMARY KEY,
    total_sales DOUBLE PRECISION
);
```

## 📊 Monitoring and Debugging

### View Kafka Topics
```bash
# List topics
docker exec broker kafka-topics --bootstrap-server localhost:9092 --list

# Consume messages
docker exec broker kafka-console-consumer --bootstrap-server localhost:9092 \
  --topic financial-transactions \
  --from-beginning
```

### Access PostgreSQL
```bash
docker exec -it postgres psql -U postgres -d ecommerce_db

# View transactions
SELECT * FROM transactions LIMIT 10;

# View sales by category
SELECT * FROM sales_per_category;
```

### Flink Web UI
- Access at http://localhost:8081
- Monitor job status, throughput, and task parallelism
- View task managers and logs

### Elasticsearch
- Access at http://localhost:9200
- Query indices: `curl http://localhost:9200/_aliases`

## 🛑 Stopping Services

To stop all containers:

```bash
docker-compose down
```

To stop and remove all data:

```bash
docker-compose down -v
```

## 📝 Configuration

### Kafka Configuration
Edit in `docker-compose.yml`:
- Bootstrap servers: `localhost:9092`
- Topic: `financial-transactions`
- Consumer group: `flink-group`

### PostgreSQL Configuration
Edit in `docker-compose.yml`:
- Host: `localhost`
- Port: `5432`
- Default credentials: Update in the DataStreamJob.java

### Flink Configuration
In `DataStreamJob.java`:
- Batch size: 1000 records
- Batch interval: 200ms
- Max retries: 5

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## 🙋 Support

For issues, questions, or suggestions, please open an issue on GitHub or contact the project maintainers.

## 🎓 Learning Resources

- [Apache Flink Documentation](https://nightlies.apache.org/flink/flink-docs-release-1.18/)
- [Kafka Quick Start](https://kafka.apache.org/quickstart)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Elasticsearch Guide](https://www.elastic.co/guide/en/elasticsearch/reference/current/index.html)

## 📚 Related Documentation

- **Flink Streaming**: Real-time processing of unbounded data streams
- **Windowing**: Aggregating transactions over time windows
- **Backpressure Handling**: Managing data flow between source and sink
- **Checkpointing**: Ensuring exactly-once semantics and fault tolerance

---

**Project Repository**: [Flink-Realtime-Streaming](https://github.com/CoolkidSenpai05/Flink-Realtime-Streaming)  
**Created by**: CoolkidSenpai05
