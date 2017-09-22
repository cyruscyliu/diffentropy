# coding=utf-8import warningsimport matplotlib.pyplot as pltimport numpy as npimport toolsfrom week2.est_entro import est_entro_JVHWwarnings.filterwarnings('ignore')def f1(x):    if x < 0 or x > 1:        return 0    elif 1 / 4 > x or x >= 3 / 4:        return 0    elif 1 / 4 <= x < 1 / 2:        return 16 * (x - 1 / 4)    elif 1 / 2 <= x < 3 / 4:        return -16 * (x - 3 / 4)def f(x):    if 0 <= x < 0.25:        return float(0)    elif 0.25 <= x < 0.5:        return 16.0 * (x - 0.25)    elif 0.5 <= x < 0.75:        return -16.0 * (x - 0.75)    elif 0.75 < x <= 1:        return float(0)    else:        raise ValueError('value should in [0, 1], now is {0}'.format(x))def MCMC_SD(size=100):    """    Assume X~U(0, 1) with only 1 dimension, then generate lots of that X,    if acceptable, add it to the result set, if not, add last X.    """    result = []    current = 0.5    for i in range(0, size):        next_ = np.random.rand()        u = np.random.rand()        if f(current) == float(0):            condition = 0        else:            condition = min(f(next_) / f(current), 1)        if u < condition:            # accept            result.append(next_)            current = next_        else:            # refuse            result.append(current)    return resultdef sampler(size, times):    results = []    for i in range(0, times):        results.append(MCMC_SD(size))    return resultsmc_times = 50record_n = np.array([100000, 10000, 1000, 100])# record_n = np.array([100])# record_h = np.array(#      [1.0 / 20, 1.0 / 19, 1.0 / 18, 1.0 / 17, 1.0 / 16,#       1.0 / 15, 1.0 / 14, 1.0 / 13, 1.0 / 12, 1.0 / 11])record_h = np.array(    [1.0 / 10000000, 1.0 / 1000000, 1.0 / 100000,     1.0 / 10000, 1.0 / 1000, 1.0 / 100,     1.0 / 15, 1.0 / 5, 1.0 / 4, 1.0 / 3, 1.0 / 2, 1.0])num = len(record_h)true = 0.5 * (1 - 4 * np.log(2)) / np.log(2)JVHW_err = np.zeros(num)fig, ax = plt.subplots()for n in record_n:    print 'begin sampler'    tmp_sample = sampler(n, times=mc_times)    print 'end sampler'    for i, h in enumerate(record_h):        S = int(1 / h)        edges = np.linspace(0, 1, S + 1)        samp = np.digitize(tmp_sample, edges)        record_JVHW = est_entro_JVHW(samp) - np.log2(S)        JVHW_err[i] = np.sqrt(np.mean(np.square(record_JVHW - true)))    print 'Calculation of n={0} has finished.'.format(n)    print ':'.join([str(JVHW_err[j]) for j in range(0, len(JVHW_err))])    ax.plot(record_h, JVHW_err, 's-', linewidth=1.5)# plt.legend(['$n=100,000$', '$n=10,000$', '$n=1,000$', '$n=100$'],#            loc='upper right')# plt.xscale('log')# ax.set_xlabel('h')# ax.set_ylabel('RMSE')# ax.set_xticks(#     [1.0 / 10000, 1.0 / 1000, 1.0 / 100, 1.0 / 50,#      1.0 / 20, 1.0 / 17, 1.0 / 15, 1.0 / 13, 1.0 / 10,#      1.0 / 5, 1.0 / 4, 1.0 / 3, 1.0 / 2, 1.0])# plt.savefig('redo_1_1')# plt.show()# 