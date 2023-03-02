from flask import Flask, render_template, request
import datetime
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from blog_scraper import BlogScraper

load_dotenv()

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.microblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            entry_title = request.form.get("title")
            entry_category = request.form.get("category")
            
            formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"title": entry_title, "content": entry_content, "date": formatted_date, "category": entry_category})

        # if input("Do you want to add a scraped blog? ").lower().startswith("y"):
        #     url = input("Ok then, provide the url of the blog post: ")
        #     title_select = input("Please give me a selector for the title: ")
        #     content_select = input("Please give me a selector for the content: ")
        #     blog_scraper = BlogScraper(url, title_select, content_select)
        #     title, content = blog_scraper.find_elements()
        #     formatted_date = datetime.datetime.today().strftime("%Y-%m-%d")
        #     app.db.entries.insert_one({"title": title, "content": content, "date": formatted_date, "category": "Scraped"})


        entries_with_date = [
            (
                entry["title"],
                entry["content"], 
                entry["date"], 
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d"),
                entry["category"]
            )
            for entry in app.db.entries.find({})
        ]
        entries_with_date.reverse()

        return render_template("home.html", entries=entries_with_date)
    return app
