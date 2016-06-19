# -*- coding: utf-8 -*-
'''
Recreating the graphs/tables found in
http://fivethirtyeight.com/features/should-travelers-avoid-flying-airlines-that-have-had-crashes-in-the-past/
'''
import numpy as np
import pandas
import seaborn as sns
from scipy import stats

def recreate():
    airline_data = pandas.read_csv('./airline-safety.csv')

    # All data in the article is per 1 trillion seat kilometers per year
    # 52 weeks in a year, each period had 14.5 years in it
    # (I would think 15, but using 14.5 makes the numbers map to the first chart of the article)
    seat_kms_flown = (airline_data['avail_seat_km_per_week'] * 52 * 14.5)
    scaling_factor = 1e12 / seat_kms_flown

    # Fatalities by Airline Are Highly Unpredictable graph
    airline_data['fatalities_85_99_per_1_trillion_sk'] = airline_data['fatalities_85_99'] * scaling_factor
    airline_data['fatalities_00_14_per_1_trillion_sk'] = airline_data['fatalities_00_14'] * scaling_factor
    lin_plot = sns.regplot(
        x=airline_data['fatalities_85_99_per_1_trillion_sk'],
        y=airline_data['fatalities_00_14_per_1_trillion_sk'],
        ci=0,
    )
    lin_plot.set_title(
        '''
        Fatalities adjusted for seats available and distance traveled
        (deaths per 1 trillion seat kilometers)
        '''
    )
    lin_plot.axes.set_xlabel('1985-99')
    lin_plot.axes.set_xlim(-50,)
    lin_plot.axes.set_ylabel('2000-14')
    lin_plot.axes.set_ylim(-50,)
    # sns.plt.show()

    # Incidents by Airline Are Slightly Predictable graph
    airline_data['incidents_85_99_per_1_trillion_sk'] = airline_data['incidents_85_99'] * scaling_factor
    airline_data['incidents_00_14_per_1_trillion_sk'] = airline_data['incidents_00_14'] * scaling_factor
    lin_plot = sns.regplot(
        x=airline_data['incidents_85_99_per_1_trillion_sk'],
        y=airline_data['incidents_00_14_per_1_trillion_sk'],
        ci=0,
    )
    lin_plot.set_title(
        '''
        Incidents adjusted for seats available and distance traveled
        (incidents per 1 trillion seat kilometers)
        '''
    )
    lin_plot.axes.set_xlabel('1985-99')
    lin_plot.axes.set_xlim(-5,)
    lin_plot.axes.set_ylabel('2000-14')
    lin_plot.axes.set_ylim(-5,)
    # sns.plt.show()

    # Calculate safety score as defined in article
    airline_data['fatal_accidents_85_99_per_1_trillion_sk'] = (
        airline_data['fatal_accidents_85_99'] * scaling_factor
    )
    airline_data['fatal_accidents_00_14_per_1_trillion_sk'] = (
        airline_data['fatal_accidents_00_14'] * scaling_factor
    )

    average_fatality_rate_85_99 = np.average(
        airline_data[['fatalities_85_99']].sum(axis=1)
    )
    average_fatal_accident_rate_85_99 = np.average(
        airline_data[['fatal_accidents_85_99']].sum(axis=1)
    )
    average_incident_rate_85_99 = np.average(
        airline_data[['incidents_85_99']].sum(axis=1)
    )
    average_fatality_rate_00_14 = np.average(
        airline_data[['fatalities_00_14']].sum(axis=1)
    )
    average_fatal_accident_rate_00_14 = np.average(
        airline_data[['fatal_accidents_00_14']].sum(axis=1)
    )
    average_incident_rate_00_14 = np.average(
        airline_data[['incidents_00_14']].sum(axis=1)
    )

    # sample_size_factor = (seat_kms_flown / 2).pow(.5)
    sample_size_factor = airline_data['avail_seat_km_per_week'].pow(.5)
    airline_data['fatalities_component_85_99'] = (
        stats.zscore(
            (
                average_fatality_rate_85_99 -
                airline_data['fatalities_85_99_per_1_trillion_sk']
            ) * sample_size_factor
        )
    )
    airline_data['fatal_accidents_component_85_99'] = (
        stats.zscore(
            (
                average_fatal_accident_rate_85_99 -
                airline_data['fatal_accidents_85_99_per_1_trillion_sk']
            ) * sample_size_factor
        )
    )
    airline_data['incidents_component_85_99'] = (
        stats.zscore(
            (
                average_incident_rate_85_99 -
                airline_data['incidents_85_99_per_1_trillion_sk']
            ) * sample_size_factor
        )
    )
    airline_data['safety_score_85_99'] = (
        airline_data[[
            'fatalities_component_85_99',
            'fatal_accidents_component_85_99',
            'incidents_component_85_99'
        ]].mean(axis=1)
    )

    airline_data['fatalities_component_00_14'] = (
        stats.zscore(
            (
                average_fatality_rate_00_14 -
                airline_data['fatalities_00_14_per_1_trillion_sk']
            ) * sample_size_factor
        )
    )
    airline_data['fatal_accidents_component_00_14'] = (
        stats.zscore(
            (
                average_fatal_accident_rate_00_14 -
                airline_data['fatal_accidents_00_14_per_1_trillion_sk']
            ) * sample_size_factor
        )
    )
    airline_data['incidents_component_00_14'] = (
        stats.zscore(
            (
                average_incident_rate_00_14 -
                airline_data['incidents_00_14_per_1_trillion_sk']
            ) * sample_size_factor
        )
    )
    airline_data['safety_score_00_14'] = (
        airline_data[[
            'fatalities_component_00_14',
            'fatal_accidents_component_00_14',
            'incidents_component_00_14'
        ]].mean(axis=1)
    )

    # The exact scores computed do not exactly match the scores in the table provided in the article.
    # The spirit of the orderings is correct, and withouth knowing the *exact* underlying methodology
    # it would be very difficult to exactly rebuild the table.
    airline_data['safety_score'] = airline_data[['safety_score_85_99', 'safety_score_00_14']].mean(axis=1)
    print airline_data.sort(['safety_score'], ascending=0)[['airline', 'safety_score']]

if __name__ == '__main__':
    recreate()
