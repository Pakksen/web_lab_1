from flask import Flask

app = Flask(__name__)

if __name__ == 'main':
  app.run(debug=True)

from structures.views import index