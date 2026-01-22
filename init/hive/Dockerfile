FROM apache/hive:4.0.0

USER root
ARG MYSQL_CONNECTOR_VERSION=8.0.33

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /opt/hive/auxlib && \
    curl -L -o /opt/hive/auxlib/mysql-connector-j-${MYSQL_CONNECTOR_VERSION}.jar \
    https://repo1.maven.org/maven2/mysql/mysql-connector-java/${MYSQL_CONNECTOR_VERSION}/mysql-connector-java-${MYSQL_CONNECTOR_VERSION}.jar

USER hive
