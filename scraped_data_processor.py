import pandas as pd

def get_unique_monster_reward_conditions(csv_file_path):
    data_set = pd.read_csv(csv_file_path, header=None)
    conditions = data_set.iloc[:, 1]
    unique_conditions = pd.unique(conditions)
    return unique_conditions


unique_conditions = get_unique_monster_reward_conditions('scraped_data/monster_rewards.csv')
for condition in unique_conditions:
    print(condition)
