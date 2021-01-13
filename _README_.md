# cxflow - Secunity's XFlow Filter 
Secunity's XFlow (Netflow/sFlow/Ipfix) filter by account networks

Built on top of [pmacct/pmacct](https://github.com/pmacct/pmacct) - see [/docker](https://github.com/secunity/cxflow1/docker) folder 

Instructions 

### Script/Config Arguments
```shell script
$ ./worker.py -h
usage: worker.py [-h] [-c CONFIG] [-l LOGFILE] [-v VERBOSE]
                 [--to_stdout TO_STDOUT] [--to_stderr TO_STDERR]
                 [--identifier IDENTIFIER] [-s HOST] [-n VENDOR] [-p PORT]
                 [-u USER] [-w PASSWORD] [-k KEY_FILENAME]
                 [--command_prefix COMMAND_PREFIX] [--url URL]
                 [--url_scheme URL_SCHEME] [--url_host URL_HOST]
                 [--url_port URL_PORT] [--url_path URL_PATH]
                 [--url_method URL_METHOD]


Secunity On-Prem Agent

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        Config file (overriding all other options)
  -l LOGFILE, --logfile LOGFILE
                        File to log to. default:
  -v VERBOSE, --verbose VERBOSE
                        Indicates whether to log verbose data
  -s HOST, --host HOST, --ip HOST
                        Router IP
  -p PORT, --port PORT  SSH port
  -n VENDOR, --vendor VENDOR  The netwrk device vendor (default "cisco")
  -u USER, --user USER, --username USER
                        SSH user
  -w PASSWORD, --password PASSWORD
                        SSH password
  -k KEY_FILENAME, --key_filename KEY_FILENAME
                        SSH Key Filename
  --identifier IDENTIFIER, --id IDENTIFIER
                        Device ID
  --url URL             The URL to use for remove server
  --url_scheme URL_SCHEME
                        Remote server URL scheme
  --url_host URL_HOST   Remote server URL hostname
  --url_port URL_PORT   Remote server URL port
  --url_path URL_PATH   Remote server URL path
  --url_method URL_METHOD
                        Remote server URL method

```

| Name | Mandatory | Description | Default |
| --- | --- | --- | --- |
| config | | Full path to config file | /opt/routers-stats-fetcher/routers-stats-fetcher.conf |
| logfile | | Full path to log file | no file is used |
| verbose | | Indicates whether to perform verbose logging | false |
| host | V | Network device hostname/ip | |
| port | | Port to use for SSH session | 22 |
| vendor | | The network device vendor | cisco |
| user | V | Username to use for SSH session | |
| password | | Password to use for SSH session | |
| key_filename | | Key file (full path) to use for SSH session | |
| identifier | V | Unique network device identifier as obtained from view network device | | 
| url | | The URL to use for sending information back to DDoS Inhibitor |

* If no config file location is specified the default config file location is used
* Parameters from config file **override** command line arguments


## Running the agent
**There are 3 options to run the agent:**
* **[Building and Running a Docker Container](#Building-and-Running-a-Docker-Container)**<br>
* **[Running a Pre-Built Docker Image](#Running-a-Pre-Built-Docker-Image)**<br>
* **[Python Script with Virtual Environment](#Python-Script-with-Virtual-Environment)**

### Building and Running a Docker Container
This is the recommended method at the moment as it does not require keeping the config file on the host machine.

1. Download the Dockerfile from which to build the local image (see [Dockerfile](Dockerfile))
```shell script
$ curl -L https://github.com/secunity/routers-stats-fetcher/raw/master/Dockerfile -o Dockerfile
```

2. Build the local image (replace *IMAGE_NAME*)
```shell script
$ docker build --rm -t IMAGE_NAME .
```

3. Download the config file
```shell script
$ curl -L https://github.com/secunity/routers-stats-fetcher/raw/master/routers-stats-fetcher.conf -o routers-stats-fetcher.conf
```

4. Edit the config file with your favorite editor
```shell script
$ vi routers-stats-fetcher.conf
```

5. Create a new container from the local image (replace *CONTAINER_NAME*).

```shell script
$ docker create -it \
--name CONTAINER_NAME \
--restart unless-stopped \
--network host \
IMAGE_NAME
```

6. Copy the edited config file inside the docker container
```shell script
$ docker cp routers-stats-fetcher.conf CONTAINER_NAME:/opt/routers-stats-fetcher/routers-stats-fetcher.conf
```

7. Start the container
```shell script
$ docker start CONTAINER_NAME
```

### Python Script with Virtual Environment
While it may look easier to setup you must make sure the script must be continuously running - 
it is utilizing an internal scheduler for that purpose.
Using a process control system (such as [supervisord](http://supervisord.org/)) is highly recommended.

1. Create the python virtual environment
 ```shell script
$ python3 -m virtualenv venv
```

2. Active virtual environment
```shell script
$ source venv/bin/activate
```

3. Install the requirements
```shell script
$ pip install -r https://github.com/secunity/routers-stats-fetcher/raw/master/requirements.txt
``` 

4. Download and edit the config file
```shell script
$ curl -L https://github.com/secunity/routers-stats-fetcher/raw/master/routers-stats-fetcher.conf -o routers-stats-fetcher.conf
$ vi routers-stats-fetcher.conf
```

5. Download the python script
```shell script
$ curl -L https://github.com/secunity/routers-stats-fetcher/blob/master/worker.py -o worker.py
```

6. Change the script run permissions
```shell script
$ chmod 777 worker.py
```

7. Run the script
```shell script
$ python worker.py
``` 

### Running a Pre-Built Docker Image
Will be added soon