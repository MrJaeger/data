# -*- coding: utf-8 -*-
'''
Recreating the graphs/data found in
http://fivethirtyeight.com/features/straight-outta-compton-is-the-rare-biopic-not-about-white-dudes
'''
import matplotlib.pyplot as plt
import numpy as np
import pandas
import seaborn as sns
from scipy import stats

def recreate():
    biopic_data = pandas.read_csv('./biopics.csv')
    biopic_data.index = pandas.Int64Index(biopic_data['year_release'])

    # Paragraph starting "Apparently, the people with important lives"
    white_races = ['White', 'Hispanic (White)', 'Middle Eastern (White)']
    white_percentage = (
        float(biopic_data[
            (biopic_data['race_known'] == 'Known') &
            (biopic_data['subject_race'].isin(white_races))
        ].shape[0]) /
        biopic_data[biopic_data['race_known'] == 'Known'].shape[0]
    )
    print (
        '{} percent of biopicture subjects whose race or ethnicity I was able to determine have been white'
        .format(white_percentage * 100)
    )

    male_percentage = float(biopic_data[biopic_data['subject_sex'] == 'Male'].shape[0]) / biopic_data.shape[0]
    print '{} percent of subjects have been men'.format(male_percentage * 100)

    # Biopic Subjects Are Mostly White graph
    years = range(1915, 2015)
    white_biopics = (
        biopic_data[(biopic_data['race_known'] == 'Known') & (biopic_data['subject_race'].isin(white_races))]
        .groupby('year_release')
        .size()
        .reindex(years, fill_value=0)
    )
    non_white_biopics = (
        biopic_data[(biopic_data['race_known'] == 'Known') & ~(biopic_data['subject_race'].isin(white_races))]
        .groupby('year_release')
        .size()
        .reindex(years, fill_value=0)
    )
    unknown_biopics = (
        biopic_data[(biopic_data['race_known'] == 'Unknown')]
        .groupby('year_release')
        .size()
        .reindex(years, fill_value=0)
    )

    sns.set_style("white")

    fig, ax1 = plt.subplots(1,1)

    first_bar = (white_biopics + non_white_biopics + unknown_biopics).tolist()
    second_bar = (non_white_biopics + unknown_biopics).tolist()
    third_bar = non_white_biopics.tolist()

    sns.barplot(x=years, y=first_bar, color='#C45E9A', ax=ax1)
    sns.barplot(x=years, y=second_bar, color='#9A9798', ax=ax1)
    sns.barplot(x=years, y=third_bar, color='#76B75B', ax=ax1)

    male_biopics = (
        biopic_data[biopic_data['subject_sex'] == 'Male']
        .groupby('year_release')
        .size()
        .reindex(years, fill_value=0)
    )
    female_biopics = (
        biopic_data[biopic_data['subject_sex'] == 'Female']
        .groupby('year_release')
        .size()
        .reindex(years, fill_value=0)
    )

    fig, ax2 = plt.subplots(1,1)

    first_bar = (male_biopics + female_biopics).tolist()
    second_bar = female_biopics.tolist()

    sns.barplot(x=years, y=first_bar, color='#F7BC7C', ax=ax2)
    sns.barplot(x=years, y=second_bar, color='#6A4E99', ax=ax2)

    sns.plt.show()

if __name__ == '__main__':
    recreate()
