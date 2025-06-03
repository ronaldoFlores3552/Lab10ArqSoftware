from flask import Flask
from routes import bp as search_api_bp
from logger import setup_logger
from datetime import datetime

app = Flask(__name__)
logger = setup_logger()

app.register_blueprint(search_api_bp)

if __name__ == '__main__':
    logger.info(f"{datetime.now().isoformat()}|SEARCH_API_SERVICE|SYSTEM|startup Service starting on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
