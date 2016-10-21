from flask import Flask, render_template, request
import os
# from intro_to_flask import app

# port = int(os.environ.get("PORT", 5000))
# app.run(debug=True, host='0.0.0.0', port=port)

app = Flask(__name__)

@app.route('/')

def home():
    return render_template('home.html')

if __name__ == '__main__':
  app.run()
