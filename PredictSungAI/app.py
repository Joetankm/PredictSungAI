from flask import Flask, request, jsonify, render_template
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from flask_cors import CORS
from mapPredict import train_model, estimate_resources
from ucsAlgo import find_shortest_path

app = Flask(__name__)
CORS(app)  # <- This enables CORS for all routes

dataset = pd.read_csv("flood.csv")
X = dataset[['Rainfall', 'Elevation', 'ForestCover', 'Urbanization', 'SoilMoisture']]
Y = dataset['FloodRisk']

x_train, x_test, y_train, y_test = train_test_split(X, Y, test_size=0.2, random_state=1)

data_split = {
    'train': {'attributes': x_train, 'target': y_train},
    'test': {'attributes': x_test, 'target': y_test}
}

model = DecisionTreeRegressor(max_depth=5)
## training
model.fit(data_split['train']['attributes'], data_split['train']['target'])

## predicting
predicts = model.predict(data_split['test']['attributes'])

accuracy = model.score(data_split['test']['attributes'], data_split['test']['target'])*100

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/path')  # This must match what you're trying to open
def map_view():
    return render_template('path.html')  # Make sure map.html exists

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    input_df = pd.DataFrame([data])
    prediction = model.predict(input_df)[0]
    return jsonify({'predicted_risk': round(prediction, 2), 'accuracy': accuracy})


model2, accuracy2=train_model()

@app.route('/submit', methods=['POST'])
def submit():
    all_regions = request.json.get("regions")  # This should be an array of dicts
    highest = None
    for region in all_regions:
        flood = int(region['Flood'])
        rural = 1 if region['AreaType'] == 'Rural' else 0
        pop = int(region['Population'])
        medical = 1 if region['Medical'] == 'Available' else 0
        features = [flood, rural, pop, medical]
        priority = model2.predict([features])[0]
        region['Priority'] = priority
        region['Estimates'] = estimate_resources(region)

        if highest is None or priority > highest['Priority']:
            highest = region

    return jsonify({'highest': highest, 'accuracy': accuracy2})
    
@app.route('/ucsPath', methods=['POST'])
def ucsPath():
    data = request.get_json()
    start = data.get("start")
    goal = data.get("goal")

    if not start or not goal:
        return jsonify({"error": "Missing start or goal"}), 400

    path, cost = find_shortest_path(start, goal)
    return jsonify({
        "path": path,
        "cost": cost
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
