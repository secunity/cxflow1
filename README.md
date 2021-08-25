# cxflow - Secunity's XFlow Filter 
Secunity's XFlow (Netflow/sFlow/Ipfix) filter by account networks

Built on top of [pmacct/pmacct](https://github.com/pmacct/pmacct) - see [/docker](https://github.com/secunity/cxflow1/docker) folder 

## Install Instructions
cxflow runs as docker container on a linux host. It accepts parameters  as environment variables.


Running the container:

```shell script
$ docker run -dit \
  --name secunity-cxflow \
  --restart unless-stopped \
  -p $LISTENING_PORT:$LISTENING_PORT/udp \
  -e "SECUNITY_IDENTIFIER=$IDENTIFIER" \
  -e "SECUNITY_PORT=$LISTENING_PORT" \
  -e "SECUNITY_PROTOCOL=$PROTOCOL" \ 
  secunity/cxflow
```

For instance, using listening port 1234 and identifier "xxxxxxxxxxxx the command should look
```shell script
$ docker run -dit \
  --name secunity-cxflow \
  --restart unless-stopped \
  -p 1234:1234/udp \
  -e "SECUNITY_IDENTIFIER=xxxxxxxxxxxx" \
  -e "SECUNITY_PORT=1234" \
  -e "SECUNITY_PROTOCOL=netflow" \
  secunity/cxflow
``` 



## Configuration options


| config key | Environment Variable Key | Mandatory | Description                    | Default                            |
| ---------- | ------------------------ | --------- | -----------                    | -------                            | 
| config     | SECUNITY_CONFIG          |           | Full path to config file       | /etc/secunity/secunity-cxflow.conf |
| identifier | SECUNITY_IDENTIFIER      | V         | Unique account identifier      |                                    |
| port       | SECUNITY_PORT            | V         | Listening UDP port             |                                    |
| protocol   | SECUNITY_PROTOCOL        |           | Protocol (netflow/sflow/ipfix) | netflow                            |
| logfile    | SECUNITY_LOGFILE         |           | Full path to log file          |                                    |
| verbose    | SECUNITY_VERBOSE         |           | Verbose logging                | false                              |



##### Docker network issue

Docker default network is 172.17.0.0/16 and the default gateway is 172.17.0.1. 

If your local network is using this range please take make the following additional step

1. 1. Create a docker network for the container. You can choose any subnet
    ```shell script
    $ docker network create \
      --subnet xxx.xxx.xxx.xxx/xxx \
      $NETWORK_NAME \
    ```
    For instance creating a network called secunity-cxflow-net using the subnet 192.168.159.0/24:
    ```shell script
    $ docker network create \
      --subnet 192.168.159.0/24 \
      secunity-cxflow-net \
    ```
2. Run the container configured to use the newly created network
    ```shell script
    $ docker run -dit \
      --name secunity-cxflow \
      --restart unless-stopped \
      --network secunity-cxflow-net \
      -p $LISTENING_PORT:$LISTENING_PORT/udp \
      -e "SECUNITY_IDENTIFIER=$IDENTIFIER" \
      -e "SECUNITY_PORT=$LISTENING_PORT" \
      -e "SECUNITY_PROTOCOL=$PROTOCOL" \ 
      secunity/cxflow
    ```
    For instance, using listening port 1234 and identifier "xxxxxxxxxxxx the command should look
    ```shell script
    $ docker run -dit \
      --name secunity-cxflow \
      --restart unless-stopped \
      --network secunity-cxflow-net \
      -p 1234:1234/udp \
      -e "SECUNITY_IDENTIFIER=xxxxxxxxxxxx" \
      -e "SECUNITY_PORT=1234" \
      -e "SECUNITY_PROTOCOL=netflow" \
      secunity/cxflow
    ``` 