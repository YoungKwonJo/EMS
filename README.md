# EMS (Elasticsearch Monitoring System)

## About

EMS is a system that monitors an Elasticsearch cluster, particularly one or more clusters that can monitor and manage the list.

## Version
```
0.1
```

## Screen Shot

### Main Page
![screen_shot_01](doc/screen_shot_01.png)

### Monitoring Page
![screen_shot_02](doc/screen_shot_02.png)

## Requirements

### Backend

1. Grafana
2. InfluxDB
3. MySQL

### Python Modules

```
pip install -r requirements.txt
```

## Architecture

EMS is consist of two main modules, one is webapp, and the other is metric worker.
![ems_arch](doc/ems_arch.png)

## Installation

### Web Application and Worker
```
git clone git@github.com:alden-kang/EMS.git
```

### Grafana Templates Import
```
doc/ElasticSearch_Disk_Used_Ratio_Overall.json.json
doc/ElasticSearch_Monitoring.json
```

## Configuration

### Web Application

```
- File : ems/webapp/config.py
```

```
class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "mysql://username:passwd@your_development_db/database_name"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	GRAFANA_HOST="your_development_grafana_url:3000"

	INFLUXDB_HOST = "your_development_influxdb"
	INFLUXDB_PORT = 8086
	INFLUXDB_USERNAME = "root"
	INFLUXDB_PASSWORD = "root"
	INFLUXDB_DATABASE = "ems_elasticsearch_monitoring"

class ProductionConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = "mysql://username:passwd@your_production_db/database_name"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
  GRAFANA_HOST="your_production_grafana_url:3000"

	INFLUXDB_HOST = "your_production_influxdb"
	INFLUXDB_PORT = 8086
	INFLUXDB_USERNAME = "root"
	INFLUXDB_PASSWORD = "root"
	INFLUXDB_DATABASE = "ems_elasticsearch_monitoring"
```

### Worker

```
- File : ems/worker/worker.conf
```

```
[DEFAULT]
SQLALCHEMY_DATABASE_URI = mysql://username:passwd@your_production_db/database_name
INFLUXDB_HOST=your_production_influxdb
INFLUXDB_PORT=8086
INFLUXDB_USERNAME=root
INFLUXDB_PASSWORD=root
INFLUXDB_DATABASE=ems_elasticsearch_monitoring
INTERVAL=60
LOGFILE=logs/worker.log
```

## How to run
It can be started by supervisord.

### Web Application

```
[program:ems-webapp]
command=env FLASK_CONFIG=production /usr/bin/gunicorn -w 8 -b 127.0.0.1:5000 manage:app --keep-alive 60 -k gevent
directory=/usr/local/ems/webapp
autostart=true
autorestart=true
redirect_stderr=true
```

### Worker

```
[program:ems-worker]
command=python worker.py
directory=/usr/local/ems/worker
user=root
```
