from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# make a mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    
	scraped_info = mongo.db.collection.find_one()

    # render an index.html template and pass collection
	return render_template("index.html", scraped_info=scraped_info)

@app.route("/scrape")
def scraper():

    # run the scrape function
    mars_info = scrape_mars.scrape()

    # drop the collection
    mongo.db.collection.drop()

    # Insert new collection
    mongo.db.collection.insert_one(mars_info)

    return redirect("http://127.0.0.1:5000/", code=302)


if __name__== '__main__':
    app.run(debug=True)