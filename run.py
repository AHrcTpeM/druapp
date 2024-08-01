from core import create_app

from settings.constants import PORT

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=PORT)