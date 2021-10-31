from app import app, socketio
import os

socketio.run(app, debug=True, port = os.environ['PORT'] if 'PORT' in os.environ else None)