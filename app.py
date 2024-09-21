from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime
import requests

app = Flask(__name__)

# Configure MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/gym_progress"
mongo = PyMongo(app)


@app.route('/')
def index():
    images_cursor = mongo.db.images.find().sort('upload_date', -1)
    images = []
    for image in images_cursor:
        filename = image['filename']
        # Handle the possibility of a missing 'upload_date'
        upload_date = image.get('upload_date')
        if upload_date and isinstance(upload_date, datetime):
            upload_date_str = upload_date.strftime('%Y-%m-%d')
        else:
            upload_date_str = 'Unknown Date'
        images.append({
            'filename': filename,
            'upload_date_str': upload_date_str
        })
    quotes = get_motivational_quotes()
    current_year = datetime.now().year
    return render_template('index.html', images=images, quotes=quotes, current_year=current_year)


@app.route('/upload', methods=['POST'])
def upload():
    if 'image' in request.files:
        image = request.files['image']
        filename = image.filename
        mongo.save_file(filename, image)
        # Store the current date and time as 'upload_date'
        mongo.db.images.insert_one({
            'filename': filename,
            'upload_date': datetime.now()
        })
    return '', 204  # Return an empty response for AJAX


@app.route('/file/<filename>')
def file(filename):
    return mongo.send_file(filename)


@app.route('/images')
def images():
    images_cursor = mongo.db.images.find().sort('upload_date', -1)
    images_list = []
    for image in images_cursor:
        filename = image['filename']
        upload_date = image.get('upload_date')
        if upload_date and isinstance(upload_date, datetime):
            upload_date_str = upload_date.strftime('%Y-%m-%d')
        else:
            upload_date_str = 'Unknown Date'
        images_list.append({
            'filename': filename,
            'upload_date_str': upload_date_str
        })
    return jsonify({'images': images_list})


def get_motivational_quotes():
    try:
        response = requests.get(
            'https://api.quotable.io/quotes?tags=inspirational&limit=3'
        )
        if response.status_code == 200:
            data = response.json()
            quotes = [f"{quote['content']} – {quote['author']}" for quote in data['results']]
            return quotes
        else:
            return ["Stay motivated!"]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching quotes: {e}")
        return ["Stay motivated!"]


if __name__ == '__main__':
    app.run(debug=True)
