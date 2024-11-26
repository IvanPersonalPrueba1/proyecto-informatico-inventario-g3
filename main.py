from api import app
import os  

# Para desarrollo:
if __name__ == '__main__':
    app.run(debug=True, host=os.environ.get("HOST", "localhost"), port=int(os.environ.get("PORT", 5000)))