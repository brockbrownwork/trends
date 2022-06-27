from pytrends.request import TrendReq
import matplotlib.pyplot as plot
import random

# hl = hosting language
# tz = timezone
pytrends = TrendReq(hl='en-US', tz=360)


keywords = ["diamonds", "opal", "rubies", "gold", "silver"]
keywords = ["diamonds", "opal", "rubies"]



keywords = ["family circus", "beetle bailey"]

keywords = ["family circus", "beetle bailey"]

keywords = ["10K rings", "14K rings"]
keywords = ["weather", "horoscopes"]
keywords = ["garfield", "putin"]
keywords = ["zales", "kay"]
# keywords = ["weather", "chance of rain"]

timeframe = '2004-01-01 2020-02-01'
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
        def fitness(guess):
            # the closer to zero, the more fit the guess is
            self.coefficient, self.offset = guess
            return self.difference_between(other_trendline)
        def mutate(guess):
            radiation = 0.5
            coefficient, offset = guess
            # TODO
            if random.random() > 0.5:
                coefficient += random.uniform(-radiation, radiation)
            else:
                offset += random.uniform(-radiation, radiation)
            return (coefficient, offset)
        # initialize random guesses for evolutionary algorithm
        population = []
        initial_population_size = 1000
        population_size = 100
        generations = 100
        for i in range(initial_population_size):
            # add random guesses to the population in the form of (coefficient, offset)
            guess = (random.uniform(0, 10), random.uniform(0, 100))
            population.append(guess)
        print("initial population", population)
        # population.sort(key = fitness)
        # self.coefficient, self.offset = population[0]
        for generation in range(generations):
            new_members = []
            for member in population:
                new_member = mutate(member)
                new_members.append(new_member)
                # print(new_member)
            population += new_members
            population.sort(key = fitness)
            population = population[:population_size]
        self.coefficient, self.offset = population[0]
    def difference_between(self, other_trendline):
        total = 0
        for i, datapoint in enumerate(self):
            total += abs(datapoint - other_trendline[i])
            # total += pow(datapoint - other_trendline[i], 2)
        average = total / len(self)
        return average # TODO
    def plot(self):
        plot.plot(range(len(self)), self, label = self.keyword)

class TrendCollection(object): # TODO
    def __init__(self, trendlines):
        self.trendlines = trendlines
    def plot(self):
        for trendline in self.trendlines:
            self.trendlines[trendline].plot()
        plot.legend()
        plot.show()

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
    trends = TrendCollection(y_data)
    first_keyword, second_keyword = list(y_data.keys())[0], list(y_data.keys())[1]
    print('difference: ', y_data[first_keyword].difference_between(y_data[second_keyword]))
    trends.plot()
    return y_data

trends = normalized_trends(keywords)
first_keyword = list(trends.keys())[0]
second_keyword = list(trends.keys())[1]
# trends[first_keyword].offset = 35
# trends[first_keyword].coefficient = 0.25

trends[first_keyword].fit_line_to(trends[second_keyword])

print("Total difference:", trends[first_keyword].difference_between(trends[second_keyword]))

for trend in trends:
    trends[trend].plot()
print('difference: ', trends[second_keyword].difference_between(trends[first_keyword]))
plot.legend()
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

