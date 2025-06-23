# import streamlit as st
# import pandas as pd
# import pickle
# from flask import Flask, render_template, request, url_for, redirect
# app=Flask(__name__)
# # Load data and models
# book_rec = pickle.load(open("book_data1.pkl", "rb"))
# model = pickle.load(open("mode.pkl", "rb"))
# vector = pickle.load(open("vector.pkl", "rb"))

# # Function to recommend books
# def recommend_book(title, n=5):
#     idx = book_rec[book_rec['Book-Title'] == title].index[0]
#     distances, indices = model.kneighbors(vector[idx], n_neighbors=n+1)
#     recommended = book_rec.iloc[indices[0][1:]][['Book-Title', 'Book-Author', 'Image-URL-M']]
#     return recommended.to_dict(orients="records")

# # Streamlit UI
# @app.route("/submit",methods=["POST"])
# def submit():
#     books=sorted(book_rec["Book-Title"].unique())

#     recomends=[]
#     required_book=request.form.get("book")
#     recomends=recommend_book(required_book)
#     return render_template("index.html",books=books,recomends=recomends)
# if __name__=="__main__":
#     app.run(debug=True)

from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

# Load data and models
book_rec = pickle.load(open("book_data1.pkl", "rb"))
model = pickle.load(open("mode.pkl", "rb"))
vector = pickle.load(open("vector.pkl", "rb"))

# Recommend function
def recommend_book(title, n=5):
    idx = book_rec[book_rec['Book-Title'] == title].index[0]
    distances, indices = model.kneighbors(vector[idx], n_neighbors=n+1)
    recommended = book_rec.iloc[indices[0][1:]][['Book-Title', 'Book-Author', 'Image-URL-S']]
    return recommended.to_dict(orient="records")

# Home route
@app.route("/", methods=["GET", "POST"])
def index():
    books = sorted(book_rec["Book-Title"].unique())
    recomends = []
    if request.method == "POST":
        required_book = request.form.get("book")
        recomends = recommend_book(required_book)
    return render_template("index.html", books=books, recomends=recomends)

if __name__ == "__main__":
    app.run(debug=True)
