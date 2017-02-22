####################################
## This code generate number of photons and charges
## according to a 2-D pdf input
## by Qing Lin
## Created @ 2017-02-21 
####################################

import sys, os
import pickle
import numpy as np
import scipy as sp
from scipy.interpolate import interp1d

class MyPhotonChargeGenerator:
    def __init__(self, Input2DFilename, g1, g2):
        self.m_pG1Value = g1
        self.m_pG2Value = g2
        self.Load(Input2DFilename)
        return

    def __eq__(self, other):
        self.m_pG1Value = other.m_pG1Value
        self.m_pG2Value = other.m_pG2Value
        # range of S1 and log
        self.m_pS1Nbins = other.m_pS1Nbins
        self.m_pS1Lower = other.m_pS1Lower
        self.m_pS1Upper = other.m_pS1Upper
        self.m_pS1Step = other.m_pS1Step
        self.m_pLogNbins = other.m_pLogNbins
        self.m_pLogLower = other.m_pLogLower
        self.m_pLogUpper = other.m_pLogUpper
        self.m_pLogStep = other.m_pLogStep
        # interpolators
        self.m_pS1Interpolator = other.m_pS1Interpolator
        self.m_pLogInterpolators = other.m_pLogInterpolators
        return


    def Load(self, Input2DFilename):
        data = pickle.load( open(Input2DFilename, 'rb') )
        if not self.CheckIfComplete(data):
            raise ValueError("Pickle file not complete")
        self.m_pS1Nbins = data['s1nbins']
        self.m_pS1Lower = data['s1lower']
        self.m_pS1Upper = data['s1upper']
        self.m_pS1Step = (self.m_pS1Upper - self.m_pS1Lower) / float( self.m_pS1Nbins)
        self.m_pLogNbins = data['lognbins']
        self.m_pLogLower = data['loglower']
        self.m_pLogUpper = data['logupper']
        self.m_pLogStep = (self.m_pLogUpper - self.m_pLogLower) / float( self.m_pLogNbins)
        # load S1 pdf and calculate cdf
        S1s = np.linspace(self.m_pS1Lower, self.m_pS1Upper, self.m_pS1Nbins+1)
        S1s = S1s[1:]
        S1PDFs = [ np.sum(A) for A in data['map'] ]
        self.m_pS1Interpolator = interp1d(np.cumsum(S1PDFs)/np.sum(S1PDFs), S1s, bounds_error=False, fill_value=(0, 1))
        # load S2 pdfs and calculate cdf
        Logs = np.linspace(self.m_pLogLower, self.m_pLogUpper, self.m_pLogNbins+1)
        Logs = Logs[1:]
        self.m_pLogInterpolators = []
        for LogPDFs in data['map']:
            self.m_pLogInterpolators.append(
                interp1d(np.cumsum(LogPDFs)/np.sum(LogPDFs), Logs, bounds_error=False, fill_value=(0,1) )
                )
        return
            

    def CheckIfComplete(self, Data):
        Items = [
                      's1nbins',
                      's1lower',
                      's1upper',
                      'lognbins',
                      'loglower',
                      'logupper',
                      'map',
                     ]
        for item in Items:
            if item not in Data:
                return False
        return True

    def GetPhotonChargeNum(self):
        s1_cdf = np.random.uniform(0, 1)
        s1 = self.m_pS1Interpolator(s1_cdf)
        s1_bin = int( (s1 - self.m_pS1Lower) / self.m_pS1Step )
        s1_bin_upper = s1_bin + 1
        if s1_bin_upper>=len(self.m_pLogInterpolators):
            s1_bin_upper = s1_bin
        s1lower = float(s1_bin)*self.m_pS1Step + self.m_pS1Lower
        s1upper = float(s1_bin_upper)*self.m_pS1Step + self.m_pS1Lower
        log_cdf = np.random.uniform(0, 1)
        loglower = self.m_pLogInterpolators[s1_bin](log_cdf)
        logupper = self.m_pLogInterpolators[s1_bin_upper](log_cdf)
        log = loglower
        if s1lower!=s1upper:
            log = (s1 - s1lower) / (s1upper - s1lower) * (logupper - loglower) + loglower
        s2 = np.power(10., log)*s1
        return (s1/self.m_pG1Value, s2/self.m_pG2Value)
        
        
        
