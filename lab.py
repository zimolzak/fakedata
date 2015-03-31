import math
import random

class LabDefinition:
    def __init__(self):
        self.roots = {}
        self.correlate_values = {}
        self.correlate_functions = {}
    def reset_root(self, rootname, how_sick = 0):
        assert 0 <= how_sick <= 1
        mu = (self.roots[rootname]['low'] + self.roots[rootname]['high']) / 2
        sigma = (self.roots[rootname]['low'] - self.roots[rootname]['high']) \
            / 2 * (how_sick + 1)
        self.roots[rootname]['value'] = random.normalvariate(mu, sigma)
    def update(self, delta, dt): # public
        # dt is a timedelta object
        for k in self.roots.keys():
            midpoint = (self.roots[k]['low'] + self.roots[k]['high']) / 2
            self.roots[k]['value'] = self.roots[k]['value'] + \
                random.normalvariate(0, midpoint * delta**2 * dt.days)
        for k in self.correlate_functions.keys():
            self.reset_correlate(k)
    def new_correlate(self, name, f, varlist, how_messy=0): # public
        self.correlate_functions[name] = \
            {'function':f, 'varlist':varlist, 'messy':how_messy}
        self.reset_correlate(name)
    def reset_correlate(self, name):
        # Takes main value, adds a little error to it, and stores f(x).
        mu = 0
        f = self.correlate_functions[name]['function']
        how_messy = self.correlate_functions[name]['messy']
        arglist = []
        for var in self.correlate_functions[name]['varlist']:
            if var in self.roots.keys():
                sigma = (self.roots[var]['high'] - self.roots[var]['low']) \
                    / 2 * how_messy
                epsilon = random.normalvariate(mu, sigma)
                arglist.append(self.roots[var]['value'] + epsilon)
            else:
                assert how_messy == 0
                arglist.append(self.correlate_values[var])
        self.correlate_values[name] = f(*arglist)
    def new_root(self, name, hardlow, low, high, hardhigh): # public
        self.roots[name] = {'hardlow':hardlow, 'low':low,
                            'high':high, 'hardhigh':hardhigh}
        self.reset_root(name)
    def sigfig(self, x, number_of_figures = 3):
        return str(round(x, number_of_figures - 1 - int(math.log10(abs(x)))))
    def contents(self, star = False): # public
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
