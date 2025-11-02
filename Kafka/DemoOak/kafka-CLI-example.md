# Kafka CLI Cheatsheet (Docker, KRaft)

Assumes container `kafka` from `confluentinc/cp-kafka:7.8.5` and broker at `localhost:9092`.

## Broker & Cluster
- Broker versions: `docker exec -it kafka kafka-broker-api-versions --bootstrap-server localhost:9092`
- Quorum status (KRaft): `docker exec -it kafka kafka-metadata-quorum --bootstrap-server localhost:9092 describe --status`
- Cluster ID: `docker exec -it kafka kafka-metadata-quorum --bootstrap-server localhost:9092 describe --status | grep -i "clusterId"`

## Topics
- List topics: `docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --list`
- Create topic (orders_topic): `docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --create --topic orders_topic --partitions 3 --replication-factor 1`
- Describe topic: `docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --describe --topic orders_topic`
- Delete topic: `docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --delete --topic orders_topic`

## Topic Config
- Show config: `docker exec -it kafka kafka-configs --bootstrap-server localhost:9092 --entity-type topics --entity-name orders_topic --describe`
- Set retention to 1 hour: `docker exec -it kafka kafka-configs --bootstrap-server localhost:9092 --entity-type topics --entity-name orders_topic --alter --add-config retention.ms=3600000`
- Enable compaction: `docker exec -it kafka kafka-configs --bootstrap-server localhost:9092 --entity-type topics --entity-name orders_topic --alter --add-config cleanup.policy=compact`

## Produce
- Simple producer (type, then Ctrl+C to exit):
  `docker exec -it kafka kafka-console-producer --bootstrap-server localhost:9092 --topic orders_topic`
- With keys (key:value per line):
  `docker exec -it kafka kafka-console-producer --bootstrap-server localhost:9092 --topic orders_topic --property parse.key=true --property key.separator=:`
- With producer properties (e.g., acks and compression):
  `docker exec -it kafka kafka-console-producer --bootstrap-server localhost:9092 --topic orders_topic --producer-property acks=all --producer-property compression.type=gzip`

## Consume
- From beginning:
  `docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic orders_topic --from-beginning`
- Print keys and timestamps:
  `docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic orders_topic --from-beginning --property print.key=true --property key.separator=":" --property print.timestamp=true`
- Read N messages then exit:
  `docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic orders_topic --max-messages 5 --from-beginning`
- As a named consumer group:
  `docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic orders_topic --group orders_cg --from-beginning`

## Consumer Groups
- List groups: `docker exec -it kafka kafka-consumer-groups --bootstrap-server localhost:9092 --list`
- Describe a group: `docker exec -it kafka kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group orders_cg`
- Reset offsets to beginning (dry-run):
  `docker exec -it kafka kafka-consumer-groups --bootstrap-server localhost:9092 --group orders_cg --topic orders_topic --reset-offsets --to-earliest --dry-run`
- Reset offsets to beginning (execute):
  `docker exec -it kafka kafka-consumer-groups --bootstrap-server localhost:9092 --group orders_cg --topic orders_topic --reset-offsets --to-earliest --execute`

## Quick Test Flow
1) Create topic: `docker exec -it kafka kafka-topics --bootstrap-server localhost:9092 --create --topic orders_topic --partitions 3 --replication-factor 1`
2) Start consumer: `docker exec -it kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic orders_topic --from-beginning`
3) Produce a few messages: `docker exec -it kafka kafka-console-producer --bootstrap-server localhost:9092 --topic orders_topic`

## Notes
- Inside the container the broker advertises `localhost:9092`; keep `--bootstrap-server localhost:9092` for CLI.
- For multi-line input or special shell features, wrap with: `docker exec -it kafka bash -lc 'your command here'`.

