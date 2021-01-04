import scipy as s
import scipy.special as special
from .basic_distributions import Distribution

# from mofapy2.core.utils import *
from mofapy2 import config

class Gamma(Distribution):
    """
    Class to define Gamma distributions

    Equations:
    p(x|a,b) = (1/Gamma(a)) * b^a * x^(a-1) * e^(-b*x)
    log p(x|a,b) = -log(Gamma(a)) + a*log(b) + (a-1)*log(x) - b*x
    E[x] = a/b
    var[x] = a/b^2
    E[ln(x)] = digamma(a) - ln(b)
    H[x] = ln(Gamma(a)) - (a-1)*digamma(a) - ln(b) + a
    """

    def __init__(self, dim, a, b, E=None, lnE=None):
        Distribution.__init__(self, dim)

        # Initialise parameters
        if isinstance(a, (int, float)):
            a = s.ones(dim) * a
        if isinstance(b, (int, float)):
            b = s.ones(dim) * b
        self.params = { 'a':a, 'b':b }

        # Initialise expectations
        if (E is None) or (lnE is None):
            self.updateExpectations()
        else:
            self.expectations = { 'E':s.ones(dim)*E, 'lnE':s.ones(dim)*lnE }

        # float64 -> float32
        if config["use_float32"]: self.to_float32()

        # Check that dimensionalities match
        self.CheckDimensionalities()

    def updateExpectations(self):
        E = self.params['a']/self.params['b']
        lnE = special.digamma(self.params['a']) - s.log(self.params['b'])
        self.expectations = { 'E':E, 'lnE':lnE }

    def density(self, x):
        assert x.shape == self.dim, "Problem with the dimensionalities"
        return s.prod( (1/special.gamma(self.params['a'])) * self.params['b']**self.params['a'] * x**(self.params['a']-1) * s.exp(-self.params['b']*x) )

    def loglik(self, x):
        assert x.shape == self.dim, "Problem with the dimensionalities"
        return s.sum( -s.log(special.gamma(self.params['a'])) + self.params['a']*s.log(self.params['b']) + (self.params['a']-1)*s.log(x) -self.params['b']*x )

    def sample(self, n=1):
        k = self.params['a']
        theta = 1./self.params['b']  # using shape/scale parametrisation
        return np.random.gamma(k, scale=theta)
