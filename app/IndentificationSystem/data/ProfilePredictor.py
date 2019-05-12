import numpy as np
from app.IndentificationSystem import data_handler
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import silhouette_score as ss
from app.IndentificationSystem.data.DataHandler import DataHandler


class ProfilePredictor:
    def __init__(self, data, learning_data, fuzzy):
        self.data = data
        self.grouped_data = learning_data
        self.fuzzy = fuzzy

    # for x in range(0, len(data_handler.param1)):
    #     second.append(list([data_handler.param1[x], data_handler.param2[x]]))
    #
    # sec_data = np.array(second)
    # sec_datapd = pd.DataFrame(sec_data)
    # scores = []
    # # print(second_data.param1)
    # max_values = []
    # min_values = []
    def get_profile(self, fuzzy):
        min, max = self.get_bounds(self.data, self.grouped_data)
        score = self.set_labels(self.data, min, max, self.grouped_data, self.fuzzy)
        self.show_result(self.data, 4, score)

    def get_bounds(self, data, learning_data):
        max_values = []
        min_values = []
        for group_label in data['labels'].unique():
            max_param1 = np.max(learning_data[0].get_group(group_label))
            max_param2 = np.max(learning_data[1].get_group(group_label))
            min_param1 = np.min(learning_data[0].get_group(group_label))
            min_param2 = np.min(learning_data[1].get_group(group_label))
            tuple_max = (max_param1, max_param2)
            tuple_min = (min_param1, min_param2)
            max_values.append(tuple_max)
            min_values.append(tuple_min)
        return min_values, max_values

    # print(max_values)
    # print(min_values)
    # print(sec_datapd)
    def set_labels(self, data, min_values, max_values, learning_data, fuzzy):

        data['labels'] = pd.Series(fuzzy.labels_)
        for i in range(0, 40):
            for j in range(len(max_values)):
                x, y, z = data.values[i]
                max1, max2 = max_values[j]
                min1, min2 = min_values[j]
                # print(x,y)
                if x > min1 and x < max1 and y > min2 and y < max2:
                    data.set_value(i, 'labels', j)

        score = ss(data[[0, 1]], labels=data['labels'])
        return score

    def show_result(self, data, number_of_clusters, score):
        data.plot.scatter(x=0, y=1, c='labels', colormap='viridis')
        plt.xlabel("Param 1")
        plt.ylabel("Param2")
        plt.title(f'K = {number_of_clusters}, Silhouette score = {score}')
        plt.show()