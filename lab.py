import math
import random
import csv

class LabDefinition:
    # Class variables; do not appear in vars() or __dict__.
    roots = {} 
    correlate_functions = {}
    D = 0.75 # what distance to hardlow or hardhigh to move
    correlate_values = {}
    def __init__(self):
        pass
    def reset_root(self, rootname, how_sick = 0):
        assert 0 <= how_sick <= 1
        mu = (self.roots[rootname]['low'] + self.roots[rootname]['high']) / 2
        sigma = (self.roots[rootname]['low'] - self.roots[rootname]['high']) \
            / 2 * (how_sick + 1)
        x = random.normalvariate(mu, sigma)
        if x < self.roots[rootname]['hardlow']:
            x = self.roots[rootname]['hardlow']
        if x > self.roots[rootname]['hardhigh']:
            x = self.roots[rootname]['hardhigh']
        exec("self." + rootname + " = x")
    def update(self, delta, dt): # public
        # dt is a timedelta object
        for k in self.roots.keys():
            midpoint = (self.roots[k]['low'] + self.roots[k]['high']) / 2
            change = random.normalvariate(0, midpoint * delta**2 * dt.days)
            x = eval("self." + k)
            if x + change < self.roots[k]['hardlow']:
                change = self.D * (self.roots[k]['hardlow'] - x)
            elif x + change > self.roots[k]['hardhigh']:
                change = self.D * (self.roots[k]['hardhigh'] - x)
            exec("self." + k + " = x + change")
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
                arglist.append(eval("self." + var + " + epsilon"))
            else:
                assert how_messy == 0
                arglist.append(eval("self." + var))
        exec("self." + name + " = f(*arglist)")
    def new_root(self, name, hardlow, low, high, hardhigh): # public
        self.roots[name] = {'hardlow':hardlow, 'low':low,
                            'high':high, 'hardhigh':hardhigh}
        self.reset_root(name)
    def sigfig(self, x, number_of_figures = 3):
        if x > 0:
            return str(round(x, number_of_figures - 1 -
                             int(math.log10(abs(x)))))
        elif x == 0:
            return str(0)
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
                    <= eval("self." + rootname) \
                    <= self.roots[rootname]['high']):
            return " **"
        else:
            return ""


class CbcBmp(LabDefinition):
    def __init__(self):
        LabDefinition.__init__(self)
        for file in ["bmp_ranges.csv", "cbc_ranges.csv"]:
            lines = csv.reader(open(file, 'r'), delimiter=',')
            for fields in lines:
                self.new_root(fields[0], *map(float,fields[1:]))
        
        def cl_func(na, ag, hco3):
            return na - ag - hco3
        def hgb2hct(hgb):
            return 3 * hgb
        def mchc_func(hgb, hct):
            return hgb / (hct / 100)
        def rbc_func(hct, mcv):
            return 10 * hct / mcv
        def mch_func(hgb, rbc):
            return 10 * hgb / rbc
        def neut2lymph(neut):
            return random.uniform(0.66,0.72) * (100 - neut)
        def mono_func(n,l,e,b):
            m = 100 - n - l - e - b
            if m > 0:
                return m
            else:
                return 0
    
        self.new_correlate('cl', cl_func, ['na', 'ag', 'hco3'])
        self.new_correlate('hct', hgb2hct, ['hgb'], how_messy=0.3)
        self.new_correlate('rbc', rbc_func, ['hct', 'mcv']) # must be after hct
        self.new_correlate('mchc', mchc_func, ['hgb', 'hct']) # must be after hct
        self.new_correlate('mch', mch_func, ['hgb', 'rbc']) # must be after rbc
        self.new_correlate('lymph', neut2lymph, ['neut'])
        self.new_correlate('mono', mono_func, ['neut', 'lymph', 'eos', 'baso'])
