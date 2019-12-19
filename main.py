import random
import numpy as np
import pandas as pd
import datetime
import argparse
import uuid

def simulate_data():

    number_of_records = random.randint(1, 50)

    column_1 = np.random.normal(loc=100, scale=3, size=number_of_records)
    column_2 = np.random.uniform(low=0, high=100, size=number_of_records)
    column_3 = np.random.logistic(loc=50, size=number_of_records)
    column_4 = np.random.binomial(10, 0.5, number_of_records)
    column_5 = [str(uuid.uuid4()) for _ in range(0, number_of_records)]

    data_with_column_names = {
        'A': column_1,
        'B': column_2,
        'C': column_3,
        'D': column_4,
        'E': column_5
    }

    return pd.DataFrame(data_with_column_names)

def save_data(data, path):
    current_datetime = datetime.datetime.now()

    file_name = '{}simulated_data_{}_{}_{}_{}_{}.csv' \
        .format(path, current_datetime.year, current_datetime.month, current_datetime.day, current_datetime.hour, current_datetime.minute)
    data.to_csv(path_or_buf=file_name, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create some data and write it to a file.')
    parser.add_argument('--path', help='Path where the files should be stored.')

    args = parser.parse_args()
    data = simulate_data()
    save_data(data, args.path)
