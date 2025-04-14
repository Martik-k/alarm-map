from waitress import serve
from app import app, get_data, update_database
from threading import Thread


Thread(target=get_data, daemon=True).start()
Thread(target=update_database, daemon=True).start()

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)
