from flask import Flask

# Create a new Flask instance:
app = Flask(__name__)

# define the starting point of route
@app.route('/')

def are_we_here_yet():
    return 'Are we here yet?'

# in Anaconda Powershell type> set FLASK_APP=app.py
# then > flask run
# You will see:
# Running on http://127.0.0.1:5000
# You place this into your web browser, [ENTER]
