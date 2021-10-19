from flask import Flask

from markupsafe import escape
import os
import threading

app = Flask(__name__)

@app.route('/pull')
def pull():
    os.system(f"./pull.sh")
    return "Building job started. Please wait this may take some time"

if __name__ == '__main__':
    app.run()
