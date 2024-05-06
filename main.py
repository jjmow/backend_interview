# run this file for testing 
from calculation import computeROI, computeWinRate, computeMDD, computeOddsRatio, computeProfitFactor, computeSharpeRatio
from util import preprocess, loadData, printFn

if __name__ == '__main__':
    
    code, msg, data = loadData('trades.json')
    
    # parameters
    cost = 8000
    data = preprocess(data)
    riskFreeRate = 0.02 # assumption


    # calculation
    ROI     = computeROI(data, cost)
    winrate = computeWinRate(data)
    MDD     = computeMDD(data, cost)
    
    oddsRatio    = computeOddsRatio(data)
    ProfitFactor = computeProfitFactor(data)
    sharpRatio   = computeSharpeRatio(data, cost, riskFreeRate)
    
    
    # print
    printFn('ROI', ROI)
    printFn('winrate', winrate)
    printFn('MDD', MDD)
    printFn('Odds Ratio', oddsRatio)
    printFn('Profit Factor', ProfitFactor, False)
    printFn('Sharp Ratio', sharpRatio, False, True)





