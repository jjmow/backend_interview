import json
import statistics
import math

def preprocess(data):
    for i in data:
        i['fillSz']     = float(i['fillSz'])
        i['fillPx']     = float(i['fillPx'])
        i['fee']        = float(i['fee'])
        i['fillPnl']    = float(i['fillPnl'])
        i['fillIdxPx']  = float(i['fillIdxPx'])
        i['fillMarkPx'] = float(i['fillMarkPx'])
    return data

def loadData(path:str):
    with open(path) as json_file: 
        rawData = json.load(json_file)
        
        code = rawData["code"]
        msg  = rawData["msg"]
        data = rawData["data"]
    return code, msg, data

def printFn(name, value:float, percentage = True, showAllDigits = False):
    if not showAllDigits:
        if percentage:
            value = value * 100.0
            print(f'{name:<15}: {value:.2f}%')    
        else:
            print(f'{name:<15}: {value:.2f}')    
    else:
        if percentage:
            value = value * 100.0
            print(f'{name:<15}: {value}%')    
        else:
            print(f'{name:<15}: {value}')    



def computeROI (data:list, cost:float):
    netProfit = 0
    
    for trade in data:
        netProfit += trade['fee']
        netProfit += trade['fillPnl']

    return netProfit / cost 

def computeWinRate (data:list):
    totalGames = 0.0
    winningGames = 0.0

    for trade in data:
        if trade['fillPnl'] != 0:
            totalGames += 1
            if trade['fillPnl'] > 0:
                winningGames += 1
                
    return winningGames / totalGames

def computeMDD (data:list, cost:float):
    netValue = cost
    MaxValue = netValue
    MDD      = 0.0 
    
    for trade in data:
        netValue += trade['fillPnl'] + trade['fee']
        MaxValue = max(MaxValue, netValue)
        MDD      = max(MDD, (MaxValue - netValue) / MaxValue)   
        
    return MDD 

def computeOddsRatio (data:list, cost:float):
    pass

def computeProfitFactor (data:list):
    grossProfit = 0.0
    grossLoss = 0.0
    # I didn't consider fee in this case, because I think ProfitFactor only focus on the performance of your strategy.
    
    for trade in data:
        gross = trade['fillPnl']
        

        if gross > 0:
            grossProfit += gross
        else:
            grossLoss -= gross
            
    return grossProfit / grossLoss

def computeSharpeRatio (data:list, cost:float, riskFreeRate:float):
    ROI = computeROI(data, cost)
    
    prices_ETH = list(map(
        lambda x:x['fillPx'],
        [ETH for ETH in data if ETH['instId'] == "ETH-USDT-SWAP"])
    )
    
    prices_BTC = list(map(
        lambda x:x['fillPx'],
        [ETH for ETH in data if ETH['instId'] == "BTC-USDT-SWAP"])
    )
    
    STD_ETH = statistics.stdev(prices_ETH)
    STD_BTC = statistics.stdev(prices_BTC)
    
    STD = math.sqrt(STD_ETH * STD_BTC) 
    
    return (ROI - riskFreeRate) / STD
        
if __name__ == '__main__':
    code, msg, data = loadData('trades.json')
    
    cost = 8000
    data = preprocess(data)
    riskFreeRate = 0.02


    ROI     = computeROI(data, cost)
    winrate = computeWinRate(data)
    MDD     = computeMDD(data, cost)
    
    ProfitFactor = computeProfitFactor(data)
    sharpRatio   = computeSharpeRatio(data, cost, riskFreeRate)
    
    printFn('ROI', ROI)
    printFn('winrate', winrate)
    printFn('MDD', MDD)
    
    printFn('Profit Factor', ProfitFactor, False)
    printFn('Sharp Ratio', sharpRatio, False, True)





