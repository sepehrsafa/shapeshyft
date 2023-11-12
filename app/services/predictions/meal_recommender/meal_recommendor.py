import pandas as pd
import joblib
import json

final_df = pd.read_csv("./app/services/predictions/meal_recommender/preprocessed_mealplans.csv")

def recommend_meal(calorie_intake, tolerance=100):

    model = joblib.load('./app/services/predictions/meal_recommender/meal_recommendation_model.pkl')

    possible_meals = final_df[(final_df['calories'] >= calorie_intake - tolerance) &
                              (final_df['calories'] <= calorie_intake + tolerance)]

    while possible_meals.empty:
        tolerance += 50
        possible_meals = final_df[(final_df['calories'] >= calorie_intake - tolerance) &
                                  (final_df['calories'] <= calorie_intake + tolerance)]

    selected_plan = possible_meals.sample(n=1)

    breakfast_title = selected_plan['breakfast'].values[0]
    lunch_title = selected_plan['lunch'].values[0]
    dinner_title = selected_plan['dinner'].values[0]
    snacks_title = selected_plan['snacks'].values[0]

    recommendation = {
        'calorie_intake': calorie_intake,
        'meals': {
            'breakfast': breakfast_title,
            'lunch': lunch_title,
            'snacks': snacks_title,
            'dinner': dinner_title
        }
    }
    return recommendation



