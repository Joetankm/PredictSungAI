# ml_model.py
import random
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

def train_model():
    def generate_flood_data(num_samples=10000):
        data = []
        for _ in range(num_samples):
            flood = random.randint(0, 10)
            rural = random.choice([0, 1])
            pop = random.randint(100, 2000)
            medical = random.choice([0, 1])
            raw_score = flood + 2 * rural + (1 if pop > 1000 else 0) + medical
            priority = int((raw_score / 14) * 100)
            priority = max(1, min(priority, 100))
            data.append([flood, rural, pop, medical, priority])
        return data

    data = generate_flood_data()
    X = np.array([d[:4] for d in data])
    Y = np.array([d[4] for d in data])
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
    data_split = {
    'train': {'attributes': X_train, 'target': Y_train},
    'test': {'attributes': X_test, 'target': Y_test}
    }
    model = RandomForestRegressor(n_estimators=100, max_depth=3, random_state=42)
    model.fit(data_split['train']['attributes'], data_split['train']['target'])    
    accuracy = model.score(data_split['test']['attributes'], data_split['test']['target'])*100
    return model, accuracy

def estimate_resources(region):
    flood = int(region['Flood'])
    population = int(region['Population'])
    medical = region['Medical'] == "Available"

    # Example estimation logic
    food = max(1, population // 1000) * (flood // 2 + 1)
    water = max(1, population // 800) * (flood // 2 + 1)
    shelter = max(1, population // 2000) * (flood // 2 + 1)
    med_staff = 100 if medical else max(1, population // 1500)

    return {
        "Food": food,
        "Water": water,
        "Shelter": shelter,
        "MedicalStaff": med_staff
    }
