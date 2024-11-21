from api import app
import os

host = os.environ.get("HOST", "localhost")
port = int(os.environ.get("PORT", 5001))

if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_ENV') == 'development', host=host, port=port)
