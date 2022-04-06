from pytrends.request import TrendReq
import matplotlib.pyplot as plot

# hl = hosting language
# tz = timezone
pytrends = TrendReq(hl='en-US', tz=360)

keywords = ["family circus", "pearls before swine", "beetle bailey"]
keywords = ["diamonds", "opal", "rubies", "gold", "silver"]
keywords = ["diamonds", "opal", "rubies"]
keywords = ["10K rings", "14K rings"]
keywords = ["zales", "kay"]

timeframe = '2004-01-01 2008-01-01'
# timeframe = '2020-06-01 2020-06-07'

class TrendLine(object):
    '''
    Contains the keyword, the datapoints, the coefficient and the offset.
    '''
    def __init__(self, keyword, datapoints):
        self.keyword = keyword
        self.datapoints = datapoints
        self.coefficient = 1
        self.offset = 0
    def __getitem__(self, i):
        return self.coefficient * self.datapoints[i] + self.offset
    def __iter__(self):
        for datapoint in self.datapoints:
            yield self.coefficient * datapoint + self.offset
    def __len__(self):
        return len(self.datapoints)
    def fit_line_to(self, other_trendline):
        pass # TODO: the holy grail of this whole thing
    def difference_between(self, other_trendline):
        total = 0
        for i, datapoint in enumerate(self):
            total += pow((datapoint - other_trendline[i]), 2)
        average = total / len(self)
        return average # TODO
    def plot(self):
        plot.plot(range(len(self)), self, label = self.keyword)

class TrendCollection(object): # TODO
    def __init__(self, trendlines):
        self.trendlines = trendlines
    def plot(self):
        pass # TODO

def normalized_trends(keywords):
    # plots the normalized trend lines,
    # then returns the trends lines in a dictionary of the format
    # y_data[keyword] = list of datapoints in trend line
    pytrends = TrendReq(hl = "en-US", tz = 360)
    y_data = {}
    for keyword in keywords:
        pytrends.build_payload([keyword], cat = 0, timeframe = timeframe)
        data = pytrends.interest_over_time()
        data = data.reset_index()
        interest = list(data[keyword])[:-1] # trim ending zero (why is there a zero here?)
        y_data[keyword] = TrendLine(keyword, interest)
        print(interest)
        y_data[keyword].plot()
    print('difference: ', y_data['zales'].difference_between(y_data['kay']))
    plot.legend()
    plot.show()
    return y_data

trends = normalized_trends(keywords)
first_keyword = list(trends.keys())[0]
second_keyword = list(trends.keys())[1]
trends[first_keyword].offset = 35
trends[first_keyword].coefficient = 0.3
for trend in trends:
    trends[trend].plot()
print('difference: ', trends[second_keyword].difference_between(trends[first_keyword]))
plot.show()

'''
trends = normalized_trends(keywords)
trends['zales'].offset = 40
trends['zales'].coefficient = 0.5
for trend in trends:
    trends[trend].plot()
plot.show()
'''
'''
pytrends.build_payload(keywords, cat = 0, timeframe = timeframe)

data = pytrends.interest_over_time() 
data = data.reset_index()


print(list(data[keywords[0]]))

for thing in data[keywords[0]]:
    print(thing)

import matplotlib.pyplot as plot

for keyword in keywords:
    y_data = list(data[keyword])[:-1]
    plot.plot(range(len(y_data)), y_data, label = keyword)
plot.legend()
plot.show()
# fig = px.line(data, x="date", y=keywords, title='Keyword Web Search Interest Over Time')
# fig.show()
'''

