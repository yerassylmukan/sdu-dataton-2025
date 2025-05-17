import random

def add_prediction_with_ai_model(trips, query):
    for trip in trips:
        trip["is_increased"] = model_predict(trip, query)

    return trips



def model_predict(trip, query):
    return random.random() > 0.5