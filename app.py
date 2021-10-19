from flask import Flask

from markupsafe import escape
import os
import threading

app = Flask("needmedi")
app.debug = True


def build(branch):
    print(" build started")
    os.system(f"./build.sh {escape(branch)}")
    print(" build over")


@app.route('/app/<branch>')
def main(branch):
    threading.Thread(target=build, args=(branch,)).start()
    return "Building job started. Please wait this may take some time"

if __name__ == '__main__':
    app.run()
