import os

class Config:

	@staticmethod
	def init_app(app):
		pass

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

config = {
	'development' : DevelopmentConfig,
	'production' : ProductionConfig,
	'default' : DevelopmentConfig
}
