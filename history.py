from __future__ import division
import urllib2
import datetime as dt
import json


# Dates for which to get history
# day = 23
# month = 'september'
# year = 1982

history = {}
file_name = 'history'

# Create date objects Year, Month, Day
start_date = dt.datetime(2012, 12,1)
end_date = dt.datetime(2013, 3,1)

total_days = (end_date - start_date).days + 1 #inclusive 5 days

for day_number in range(total_days):
    current_date = (start_date + dt.timedelta(days = day_number)).date()
    history[str(current_date)] = []


def get_history(date):

    # Get day, month, year from str
    year = date[0:4]
    month = date[5:7]
    day = date[8:10]

    month_names = {
        '01' : 'january',
        '02' : 'february',
        '03' : 'march',
        '04' : 'april',
        '05' : 'may',
        '06' : 'june',
        '07' : 'july',
        '08' : 'august',
        '09' : 'september',
        '10' : 'october',
        '11' : 'november',
        '12' : 'december'
     }

    month_name = month_names[month]

    # Construct url
    site = 'http://www.historyorb.com/date/'
    date = str(year) + '/' + str(month_name) + '/' + str(day)
    url = site + date

    # Download url
    headers = { 'User-Agent' : 'Mozilla/5.0' }
    req = urllib2.Request(url, None, headers)
    html = urllib2.urlopen(req).read()

    # dow_start = html.find('Day of Week:')

    stop_points = []

    his_start = html.find('<h2>Historical Events</h2>')
    bds_start = html.find('<h2>Famous Birthdays</h2>')
    wed_start = html.find('<h2>Famous Weddings</h2>')
    dea_start = html.find('<h2>Famous Deaths</h2>')

    if bds_start != -1:
        stop_points.append(bds_start)
    if wed_start != -1:
        stop_points.append(wed_start)
    if dea_start != -1:
        stop_points.append(dea_start)

    if stop_points:
        stop_point = min(stop_points)
    else:
        stop_point = his_start + html[his_start:].find('<table width=')


    # Get raw sections
    # dow_raw = html[dow_start:his_start]
    his_raw = html[his_start:stop_point]

    # Process sections
    # dow = dow_raw.replace('</b>','').replace('</p>', '').replace('\n', '').replace('Day of Week: ', '')

    his_pro1 = his_raw[his_raw.find('<p>-')+4:].split('-')
    his_pro2 = []

    for line in his_pro1:
        his_pro2.append(line.replace('<br />\n', '').replace('</p>\n', '').strip(' '))

    return his_pro2

for date in history:
    print date
    history[date] = get_history(date)
    if history[date] != ['']:
        print history[date]
        print '\n'
    else:
        print 'Nothing happened.\n'

# Save to json file
f = open(file_name + '.json', 'a')
json.dump(history, f)
f.close()
