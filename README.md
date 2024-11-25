<!--
 Licensed to the Apache Software Foundation (ASF) under one
 or more contributor license agreements.  See the NOTICE file
 distributed with this work for additional information
 regarding copyright ownership.  The ASF licenses this file
 to you under the Apache License, Version 2.0 (the
 "License"); you may not use this file except in compliance
 with the License.  You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing,
 software distributed under the License is distributed on an
 "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 KIND, either express or implied.  See the License for the
 specific language governing permissions and limitations
 under the License.
-->

# Redpanda + Iceberg + Spark Quickstart Image

This is a docker compose environment to quickly get up and running with Redpanda, a Spark environment and a local REST
catalog, and MinIO as a storage backend.

**note**: If you don't have docker installed, you can head over to the [Get Docker](https://docs.docker.com/get-docker/)
page for installation instructions.

**note**: If you don't have rpk installed, you can head over to the [Install RPK](https://docs.redpanda.com/current/get-started/rpk-install/)
page for installation instructions.

## Usage
Start up the notebook server by running the following.

```shell
docker compose build && docker compose up
```

Create and switch to a new rpk profile so that you can issue rpk commands

```shell
rpk profile create docker-compose-iceberg --set=admin_api.addresses=localhost:19644 --set=brokers=localhost:19092 --set=schema_registry.addresses=localhost:18081
```

Create two topics with iceberg enabled:

```
rpk topic create topic_a --topic-config=redpanda.iceberg.mode=key_value
rpk topic create topic_b --topic-config=redpanda.iceberg.mode=value_schema_id_prefix
```

Now we can produce data against the key_value topic and see data show up.

```
echo "hello world\nfoo bar\nbaz qux" | rpk topic produce topic_a --format='%k %v\n'
```

The notebook server will then be available at http://localhost:8888 see the single notebook will guide you through querying that table.

Next we will show how the schema registry integration works. First we need to create the schema in the schema registry:

```
rpk registry schema create topic_b-value --schema schema.avsc
```

```
echo '{"user_id":2324,"event_type":"BUTTON_CLICK","ts":"2024-11-25T20:23:59.380Z"}\n{"user_id":3333,"event_type":"SCROLL","ts":"2024-11-25T20:24:14.774Z"}\n{"user_id":7272,"event_type":"BUTTON_CLICK","ts":"2024-11-25T20:24:34.552Z"}' | rpk topic produce topic_b --format='%v\n' --schema-id=topic
```

Once the data is committed, shortly the data should be available in Iceberg format and you can query the table `demo.redpanda.topic_b` in the notebook.

## Alternative query interfaces

While the notebook server is running, you can use any of the following commands if you prefer to use spark-shell, spark-sql, or pyspark.

```
docker exec -it spark-iceberg spark-shell
```
```
docker exec -it spark-iceberg spark-sql
```
```
docker exec -it spark-iceberg pyspark
```

To stop everything, just run `docker-compose down`.
