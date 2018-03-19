import os

class Config:

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(Config):
	DEBUG = True
	SQLALCHEMY_DATABASE_URI = "mysql://rackmonkey:sksmsrktnek@infra-devdb.is.daumkakao.io/rackmonkey"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	GRAFANA_HOST="infra-devdb.is.daumkakao.io:3000"

	INFLUXDB_HOST = "infra-devdb.is.daumkakao.io"
	INFLUXDB_PORT = 8086
	INFLUXDB_USERNAME = "root"
	INFLUXDB_PASSWORD = "root"
	INFLUXDB_DATABASE = "ems_elasticsearch_monitoring"


class ProductionConfig(Config):
	DEBUG = False
	SQLALCHEMY_DATABASE_URI = "mysql://rackmonkey:sksmsrktnek@infradb01.mydb.iwilab.com/rackmonkey"
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	GRAFANA_HOST="infra-devdb.is.daumkakao.io:3000"

	INFLUXDB_HOST = "infra-devdb.is.daumkakao.io"
	INFLUXDB_PORT = 8086
	INFLUXDB_USERNAME = "root"
	INFLUXDB_PASSWORD = "root"
	INFLUXDB_DATABASE = "ems_elasticsearch_monitoring"


config = {
	'development' : DevelopmentConfig,
	'production' : ProductionConfig,
	'default' : DevelopmentConfig
}
