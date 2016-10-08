'''

Created on 7/10/2016


'''
import matplotlib
matplotlib.use('Qt5Agg')

import matplotlib.pyplot as plt
from credit import *



nper = 60

linear = PrepaymentModel.linear(nper, level=0.05)
psa = PrepaymentModel.psa(nper, ceil=0.05, stable_per=24)


plt.plot(linear)
plt.plot(psa)

plt.show()



if __name__ == '__main__':
    pass