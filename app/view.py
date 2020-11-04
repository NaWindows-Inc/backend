from app import app
from models import BleData

@app.route('/')
def index():
    return 'Hello world'