from flask import Flask, render_template, send_file
from flask_cors import CORS
from GOE_climate_results import results_app
 
app = Flask(__name__)
CORS(app)

app.register_blueprint(results_app)

if __name__ == '__main__':
    app.run(debug=True, port=3000)