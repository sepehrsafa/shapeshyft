import os
import pandas as pd
import json

try:
    current_directory = os.path.dirname(os.path.abspath(__file__))
except NameError:
    current_directory = os.getcwd()

try:
    mealplans_path = os.path.join(current_directory, 'mealplans.csv')
    dishes_path = os.path.join(current_directory, 'dishes.csv')

    mealplans_df = pd.read_csv(mealplans_path)
    dishes_df = pd.read_csv(dishes_path)
    
except Exception as e:
    raise Exception(f"Error in file operations: {e}")

try:
    mealplans_columns_to_keep = ['id', 'calories', 'breakfast0', 'lunch0', 'snacks0', 'dinner0']
    mealplans_df = mealplans_df[mealplans_columns_to_keep]
    mealplans_df.dropna(subset=['breakfast0', 'lunch0', 'snacks0', 'dinner0'], inplace=True)

    dishes_df['id'] = dishes_df['id'].astype(mealplans_df['breakfast0'].dtype)
except Exception as e:
    raise Exception(f"Error processing dataframes: {e}")

try:
    breakfast_df = mealplans_df.join(dishes_df.set_index('id'), on='breakfast0', rsuffix='_breakfast')
    lunch_df = breakfast_df.join(dishes_df.set_index('id'), on='lunch0', rsuffix='_lunch')
    dinner_df = lunch_df.join(dishes_df.set_index('id'), on='dinner0', rsuffix='_dinner')
    final_df = dinner_df.join(dishes_df.set_index('id'), on='snacks0', rsuffix='_snacks')

    final_columns_to_keep = ['id', 'calories', 'title', 'title_lunch', 'title_snacks', 'title_dinner']
    final_df = final_df[final_columns_to_keep]
    final_df.rename(columns={'title': 'breakfast', 'title_lunch': 'lunch', 'title_dinner': 'dinner', 'title_snacks': 'snacks'}, inplace=True)

except Exception as e:
    raise Exception(f"Error joining dataframes: {e}")

def recommend_meal(calorie_intake, tolerance=100):
    if calorie_intake < 500:
        raise ValueError("Calorie intake must be at least 500 calories.")

    try:
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
    except Exception as e:
        raise Exception(f"Error in meal recommendation: {e}")

# Example of usage
# print(recommend_meal(input_calorie))