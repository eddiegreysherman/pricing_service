from src.app import app
import os

app.run(host="0.0.0.0", debug=app.config['DEBUG'], port=os.environ.get(port))
