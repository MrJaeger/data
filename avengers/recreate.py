# -*- coding: utf-8 -*-
'''
Recreating the analysis found in
http://fivethirtyeight.com/features/avengers-death-comics-age-of-ultron/
'''
import pandas

def recreate():
    avengers_data = pandas.read_csv('./avengers.csv')
    all_avengers = float(avengers_data.shape[0])

    # Paragraph starting with "Out of 173 listed Avengers"
    dead_avengers = avengers_data[avengers_data['Death1'] == 'YES'].shape[0]
    print '# of avengers who have died: {}'.format(dead_avengers)
    print ('% (rounded to nearest %) of all avengers who have died: {}%'
        .format(round(((dead_avengers / all_avengers) * 100), 0))
    )

    # Paragraph starting with "I counted 89 total deaths"
    deaths = 0
    recoveries = 0
    permadeaths = 0
    for num in range(1, 6):
        deaths += avengers_data[avengers_data['Death{}'.format(num)] == 'YES'].shape[0]
        recoveries += avengers_data[avengers_data['Return{}'.format(num)] == 'YES'].shape[0]
        permadeaths += (
            avengers_data.loc[
                (avengers_data['Death{}'.format(num)] == 'YES') &
                (avengers_data['Return{}'.format(num)] == 'NO')
            ]
            .shape[0]
        )

    print '# of total deaths: {}'.format(deaths)
    print '# of total recoveries: {}'.format(recoveries)

    # Paragraph starting with "Given the Avengers’ 53 years in operation"
    months_of_marvel = 53 * 12.0
    print 'Can expect a death every {} months'.format(months_of_marvel / deaths)
    print 'Can expect a permadeath every {} months'.format(months_of_marvel / permadeaths)


if __name__ == '__main__':
    recreate()
