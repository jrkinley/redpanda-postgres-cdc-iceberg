# Redpanda Connect Postgres CDC to Iceberg Demo

This is a docker compose environment to quickly demonstrate how to use Redpanda Connect's Postgres CDC connector to stream database transactions into a Redpanda Iceberg topic. Includes a MinIO storage backend, an Apache Spark environment, and a local REST catalog for querying the Iceberg tables.

This is a fork of Databricks' [Spark + Iceberg Quickstart Image](https://github.com/databricks/docker-spark-iceberg).

**note**: If you don't have a free Neon account, you can head over to [Neon](https://neon.tech/) page to sign up. After creating a database, make sure to enable Logical Replication under Settings.

**note**: If you don't have docker installed, you can head over to the [Get Docker](https://docs.docker.com/get-docker/)
page for installation instructions.

**note**: If you don't have rpk installed, you can head over to the [Install RPK](https://docs.redpanda.com/current/get-started/rpk-install/) page for installation instructions.

## Usage

### Start up environment

```shell
docker compose build && docker compose up
```

- [Redpanda Console](http://localhost:8081)
- [Jupyter Notebook](http://localhost:8888)

### Create local .env file

```shell
cat .env
NEON_PASSWORD=******
REDPANDA_BROKERS=localhost:19092
```

### Create Postgres (Neon) database

```sql
psql '<connection string>'

CREATE TABLE "quotes" (
    "id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "symbol" text NOT NULL,
    "date" date NOT NULL,
    "close" text NOT NULL,
    "volume" integer NOT NULL,
    "open" text NOT NULL,
    "high" text NOT NULL,
    "low" text NOT NULL
);

\copy quotes(symbol, date, close, volume, open, high, low) from '/path/to/redpanda-postgres-cdc-iceberg/data/AAPL_historical_max.csv' csv header;
\copy quotes(symbol, date, close, volume, open, high, low) from '/path/to/redpanda-postgres-cdc-iceberg/data/META_historical_max.csv' csv header;
\copy quotes(symbol, date, close, volume, open, high, low) from '/path/to/redpanda-postgres-cdc-iceberg/data/MSFT_historical_max.csv' csv header;

SELECT * FROM quotes LIMIT 10;

SELECT symbol, min(date) AS min_date, max(date) AS max_date, count(*)
FROM quotes
GROUP BY symbol;
```

### Create Redpanda Iceberg table

```shell
rpk profile create docker-compose-iceberg \
    --set=admin_api.addresses=localhost:19644 \
    --set=brokers=localhost:19092 \
    --set=schema_registry.addresses=localhost:18081

rpk topic create quotes --topic-config=redpanda.iceberg.mode=value_schema_id_prefix
rpk registry schema create quotes-value --schema quotes.avsc
```

### Run Postgres CDC pipeline

```shell
rpk connect run -e .env postgres-cdc.yaml
```

### Query Iceberg table from Spark

Open and run the [Jupyter Notebook](http://localhost:8888) to query the Iceberg table.

Insert a new record into the Postgres table and rerun the Spark queries to check the CDC records are streaming through:

```sql
INSERT INTO quotes
VALUES (default, 'AAPL', '2024-12-06', '$242.84', 36870620, '$242.905', '$244.63', '$242.08');
```
