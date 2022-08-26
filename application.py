from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd


item_similarity_df = pd.read_csv("sih_data.csv", index_col=0)
item_similarity_df = item_similarity_df.pivot_table(
    index="Name", columns="Habit", values="Rating")
item_similarity_df.fillna(0, inplace=True)
item_similarity_df = item_similarity_df.corr(method="pearson")
print(item_similarity_df)


app = Flask(__name__)
CORS(app)


@app.route("/")
def hello_from_root():
    return jsonify(message='Hello from root!')


@app.route("/recms", methods=["POST"])
def make_rec():
    if request.method == "POST":
        data = request.json
        habit_category = data["habit"]
        # curl -X POST http://0.0.0.0:80/recms -H 'Content-Type: application/json' -d '{"movie_title":"Heat (1995)"}'
        try:
            similar_score = item_similarity_df[habit_category]
            similar_category = similar_score.sort_values(ascending=False)[1:50]
            api_recommendations = [*set(similar_category.index.to_list())]
        except:
            api_recommendations = ["Dance", "Stay-Fit-with-Exercises", "Exercise-Time", "Call-My-Parents", "Eat-Fruits",
                                   "Go-Climbing", "Practice-for-Baseball", "Watch-Your-Diet", "Appreciate-Others", "Count-Your-Steps"]
        return {"rec_habit": api_recommendations}


# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=80)
