#################################################
# All Dependencies
#################################################

import scrape_mars
import pymongo
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo

#################################################
# Flask and MongoDB Setup
#################################################
scrape_app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

db = client.mars_data
collection = db.scrape_data


#################################################
# Flask Routes
#################################################

@scrape_app.route("/")
def index():
    # get the current data from database
    # Since the find command returns a curser obj, sending to list gets the data (!)
    mars_dictionary = list(db.scrape_data.find())

    # Since had to make a list above, need the [0]
    return render_template("index.html", mars_dictionary=mars_dictionary[0])


@scrape_app.route("/scrape")
def scraper():
    # do new scrape
    mars_dictionary = scrape_mars.scrape_all()
    # save (overwrite) the new data
    db.scrape_data.update({}, mars_dictionary)
    # refresh page
    return redirect("/", code=302)


if __name__ == "__main__":
    scrape_app.run(debug=True)