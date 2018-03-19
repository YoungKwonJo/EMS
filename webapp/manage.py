import os
from webapp import app
from flask_script import Manager

manager = Manager(app)

if __name__ == "__main__":
	app.logger.info("start server")
	manager.run()
