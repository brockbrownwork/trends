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

timeframe = '2005-01-01 2007-01-01'
# timeframe = '2020-06-01 2020-06-07'

class TrendLine(object):
    def __init__(self, keyword, datapoints):
        self.keyword = keyword
        self.datapoints = datapoints
        self.coefficient = 1
        self.offset = 0
    def __getitem__(self, i):
        return self.coefficient self.datapoints[i] + self.offset
    def __len__(self):
        return len(self.datapoints)
    def fit_line_to(self, other_trendline):
        pass # TODO
    def plot(self):
        # TODO
        plot.plot(range(len(self)), self.datapoints, label = self.keyword)

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
        y_data[keyword] = interest
        print(interest)
        plot.plot(range(len(interest)), interest, label = keyword)
    plot.legend()
    plot.show()
    return y_data

normalized_trends(keywords)



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

