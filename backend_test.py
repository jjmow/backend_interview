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
    netProfit = 0.0
    
    for trade in data:
        netProfit += trade['fee'] + trade['fillPnl']

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

def computeOddsRatio (data:list):
    winRate  = computeWinRate(data)
    lossRate = 1 - winRate
    
    return winRate / lossRate
            

def computeProfitFactor (data:list):
    grossProfit = 0.0
    grossLoss = 0.0
    # | I didn't consider fee in this case, 
    # | because I think Profit Factor only focus on the performance of our strategies.
    
    for trade in data:
        gross = trade['fillPnl']
        

        if gross > 0:
            grossProfit += gross
        else:
            grossLoss -= gross

            
    return grossProfit / grossLoss

def computeSharpeRatio (data:list, cost:float, riskFreeRate:float):
    ROI = computeROI(data, cost)
    
    # | this part I only consider std of ETH 
    # | since the problem statement only states that:
    # | " `fillSz` 值為合約張數，每張合約大小為 0.01 ETH "
    # | which means we are more focus on ETH
    
    prices_ETH = list(map(
        lambda x:x['fillPx'],
        [ETH for ETH in data if ETH['instId'] == "ETH-USDT-SWAP"])
    )
    
    # prices_BTC = list(map(
    #     lambda x:x['fillPx'],
    #     [ETH for ETH in data if ETH['instId'] == "BTC-USDT-SWAP"])
    # )
    
    STD_ETH = statistics.stdev(prices_ETH)
    # STD_BTC = statistics.stdev(prices_BTC)
    
    # q_ETH = sum(prices_ETH)
    
    # q_BTC = sum(prices_BTC)
    
    # q_total = q_ETH + q_BTC
    # STD = ((STD_ETH * q_ETH) + (STD_BTC * q_BTC)) / q_total
    
    
    
    return (ROI - riskFreeRate) / STD_ETH
        
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





