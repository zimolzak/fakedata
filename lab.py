import math
import random

class LabDefinition:
    def __init__(self, labname, low, high):
        self.roots = {}
        self.new_root(labname, low, high)
        self.correlate_values = {}
        self.correlate_functions = {}
    def reset_root(self, rootname, how_sick = 0): #may want this public
        assert 0 <= how_sick <= 1
        mu = (self.roots[rootname]['low'] + self.roots[rootname]['high']) / 2
        sigma = (self.roots[rootname]['low'] - self.roots[rootname]['high']) \
            / 2 * (how_sick + 1)
        self.roots[rootname]['value'] = random.normalvariate(mu, sigma)
    def update(self, delta, dt): # definite public
        # dt is a timedelta object
        for k in self.roots.keys():
            midpoint = (self.roots[k]['low'] + self.roots[k]['high']) / 2
            self.roots[k]['value'] = self.roots[k]['value'] + \
                random.normalvariate(0, midpoint * delta**2 * dt.days)
        for k in self.correlate_functions.keys():
            self.reset_correlate(k)
    def new_correlate(self, name, f, rootname, how_messy): # definite public
        self.correlate_functions[name] = \
            {'function':f, 'rootname':rootname, 'messy':how_messy}
        self.reset_correlate(name)
    def reset_correlate(self, name):
        # Takes main value, adds a little error to it, and stores f(x).
        mu = 0
        f = self.correlate_functions[name]['function']
        how_messy = self.correlate_functions[name]['messy']
        arglist = []
        for var in self.correlate_functions[name]['rootname']:
            sigma = (self.roots[var]['high'] - self.roots[var]['low']) \
                / 2 * how_messy
            epsilon = random.normalvariate(mu, sigma)
            arglist.append(self.roots[var]['value'] + epsilon)
        self.correlate_values[name] = f(*arglist)
    def new_root(self, name, low, high): # definite public
        self.roots[name] = {'low':low, 'high':high}
        self.reset_root(name)
    def sigfig(self, x, number_of_figures = 3):
        return str(round(x, number_of_figures - 1 - int(math.log10(abs(x)))))
    def contents(self, star = False): # definite public
        output = {}
        if star:
            for k, v in self.roots.iteritems():
                output[k] = self.sigfig(v['value']) + self.star_if_abnormal(k)
        else:
            for k, v in self.roots.iteritems():
                output[k] = self.sigfig(v['value'])
        for k, v in self.correlate_values.iteritems():
            output[k] = self.sigfig(v)
        return output
    def star_if_abnormal(self, rootname):
        if not (self.roots[rootname]['low'] \
                    <= self.roots[rootname]['value'] \
                    <= self.roots[rootname]['high']):
            return " **"
        else:
            return ""