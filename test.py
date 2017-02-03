"""
Intuit - rit-challenge

This program is used to read the user's transaction data and
on basis of the details I extract the features like has_child,
is_divorced, likes_NBA, etc.

Requirements:
Python version: 3.5
Libraries used: pandas, os

"""

__author__ = 'Vaibhav Nagda(vjn4006@rit.edu)'

import os
import pandas as pd

DIR = 'transaction-data'
files = map(lambda x: os.path.join(DIR, x), os.listdir(DIR))
files = filter(lambda x: 'csv' in x, files)


def hobbies(column):
    '''
    This method collects various hobbies using keywords like Piano, Guitar, etc.
    that a user is interested in.
    :param column: Vendor desription of all transaction of a particular user
    :return: string containing hobbies
    '''

    ans = []
    if any(column.contains("Piano")):
        ans.append("Piano")
    if any(column.contains("Guitar")):
        ans.append("Guiar")
    if any(column.contains("Bowling")):
        ans.append("Bowling")
    if any(column.contains("Ice Skating Rink")):
        ans.append("Ice Skating Rink")
    if any(column.contains("Painting")):
        ans.append("Painting")
    if any(column.contains("Museum")):
        ans.append("Museum")
    if any(column.contains("Art")):
        ans.append("Art")
    if any(column.contains("Bike")):
        ans.append("Bike")
    return ', '.join(ans)


def get_features(file_name):
    '''
    This function accumulates various features of a user
    :param file_name: an users transaction file
    :return: dictionary of features
    '''
    data = pd.read_csv(file_name)
    data.columns = ['auth_id', 'Date', 'Vendor', 'Amount', 'Location']
    features = {
        'has_child': any(data.Vendor.str.contains("Baby") | data.Vendor.str.contains("Babies")),
        'is_divorced': any(data.Vendor.str.contains("Divorce Lawyer Fees")),
        'likes_NBA': any(data.Vendor.str.contains("NBA")),
        'likes_NFL': any(data.Vendor.str.contains("NFL")),
        'has_pet': any(data.Vendor.str.contains("Pet")),
        'likes_wine': any(data.Vendor.str.contains("Wine")),
        'income': data.Amount[data.Amount > 0].max(),
        'goes_to_gym': any(data.Vendor.str.contains("Gym")),
        'goes_to_library': any(data.Vendor.str.contains("Library")),
        'hobbies': hobbies(data.Vendor.str),
    }
    features['is_student'] = (any(data.Vendor.str.contains("Student")) and
                              not features['has_child'] and
                              (any(data.Vendor.str.contains('Book')) or features['goes_to_library']))
    return features


if __name__ == '__main__':
    result = {}
    for f in files:
        result[os.path.basename(f).split('.')[0]] = get_features(f)
    users, features = zip(*result.items())
    display = pd.DataFrame(list(features), list(users))
    # To print only first five rows
    # print(display.head())

    # To print the full extracted information in a table form
    print(display)
