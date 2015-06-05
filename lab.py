import math
import random
import csv

class LabDefinition:
    def __init__(self, star=True):
        self._roots = {}
        self._correlate_values = {}
        self._correlate_functions = {}
        self._D = 0.75 # what distance to hardlow or hardhigh to move
        self._star = star
    def new_root(self, name, hardlow, low, high, hardhigh): # public
        """Add a new root to the lab panel.

        name is a string for naming the new root. low and high
        describe the lab's normal range, a.k.a. reference range.
        hardlow and hardhigh describe limits beyond which the lab is
        NEVER allowed to go.
        """
        self._roots[name] = {'hardlow':hardlow, 'low':low,
                            'high':high, 'hardhigh':hardhigh}
        self.reset_root(name)
    def reset_root(self, rootname, how_sick = 0):
        """Give rootname a new value, chosen from a normal distribution,
        independent of any prior values. how_sick ranges from 0 to 1.
        Higher values widen the standard deviation of the
        distribution.
        """
        assert 0 <= how_sick <= 1
        mu = (self._roots[rootname]['low'] + self._roots[rootname]['high']) / 2
        sigma = (self._roots[rootname]['low'] - self._roots[rootname]['high']) \
            / 2 * (how_sick + 1)
        x = random.normalvariate(mu, sigma)
        if x < self._roots[rootname]['hardlow']:
            x = self._roots[rootname]['hardlow']
        if x > self._roots[rootname]['hardhigh']:
            x = self._roots[rootname]['hardhigh']
        self._roots[rootname]['value'] = x
        self.assign_pretty_print(rootname)
    def new_correlate(self, name, f, varlist, how_messy=0): # public
        """Add a new correlate to the lab panel.

        name is a string for naming the new correlate. f is a function
        that defines how to calculate the correlate. varlist is a list
        of strings that describes which roots and/or correlates to
        plug in to the arguments of f. how_messy determines what
        amount of noise to add to the root(s) of the new correlate.
        """
        self._correlate_functions[name] = \
            {'function':f, 'varlist':varlist, 'messy':how_messy}
        self.reset_correlate(name)
    def reset_correlate(self, name):
        """Recalculate a correlate from anything it depends on. The generating
        function, etc. do not need to be re-specified.
        """
        mu = 0
        f = self._correlate_functions[name]['function']
        how_messy = self._correlate_functions[name]['messy']
        arglist = []
        for var in self._correlate_functions[name]['varlist']:
            if var in self._roots.keys():
                sigma = (self._roots[var]['high'] - self._roots[var]['low']) \
                    / 2 * how_messy
                epsilon = random.normalvariate(mu, sigma)
                arglist.append(self._roots[var]['value'] + epsilon)
            else:
                assert how_messy == 0
                arglist.append(self._correlate_values[var])
        self._correlate_values[name] = f(*arglist)
        self.assign_pretty_print(name)
    def update(self, delta, dt): # public
        """Update all roots and correlates to value number N+1, based on value
        number N and a certain time interval. delta is a Brownian
        motion parameter. dt is a timedelta object.

        After initial setup of roots and correlates, this is typically
        the only method that is called.
        """
        for k in self._roots.keys():
            midpoint = (self._roots[k]['low'] + self._roots[k]['high']) / 2
            change = random.normalvariate(0, midpoint * delta**2 * dt.days)
            x = self._roots[k]['value']
            if x + change < self._roots[k]['hardlow']:
                change = self._D * (self._roots[k]['hardlow'] - x)
            elif x + change > self._roots[k]['hardhigh']:
                change = self._D * (self._roots[k]['hardhigh'] - x)
            self._roots[k]['value'] = x + change
            self.assign_pretty_print(k)
        for k in self._correlate_functions.keys():
            self.reset_correlate(k)
    def sigfig(self, x, number_of_figures = 3):
        """Take a float and return a string with the given number of
        significant figures.
        """
        if x > 0:
            return str(round(x, number_of_figures - 1 -
                             int(math.log10(abs(x)))))
        elif x == 0:
            return str(0)
    def star_if_abnormal(self, rootname):
        """Return two stars if the given root is outside its normal range."""
        if not (self._roots[rootname]['low'] \
                    <= self._roots[rootname]['value'] \
                    <= self._roots[rootname]['high']):
            return " **"
        else:
            return ""
    def assign_pretty_print(self, labname):
        """Update the publicly visible instance variable (string) for the
        given root or correlate.
        """
        if labname in self._roots.keys():
            if self._star:
                str = self.sigfig(self._roots[labname]['value']) + \
                    self.star_if_abnormal(labname)
            else:
                str = self.sigfig(self._roots[labname]['value'])
        elif labname in self._correlate_values.keys():
            str = self.sigfig(self._correlate_values[labname])
        exec("self." + labname + " = '" + str + "'")

class CbcBmp(LabDefinition):
    def __init__(self, star=True):
        LabDefinition.__init__(self, star)
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
