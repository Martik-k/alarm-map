from waitress import serve
from app import app, get_data
from threading import Thread


data_thread = Thread(target=get_data)
data_thread.start()

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)
