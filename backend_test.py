import json

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

def printFn(name, value:float, percentage = True):
    if percentage:
        value = value * 100.0
        print(f'{name:<10}: {value:.2f}%')    
    else:
        print(f'{name}: {value:.2f}')    




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

def computeProfitFactor (data:list, cost:float):
    pass

def computeSharpeRatio (data:list, cost:float):
    pass   
        
if __name__ == '__main__':
    code, msg, data = loadData('trades.json')
    
    cost = 8000
    data = preprocess(data)


    ROI     = computeROI(data, cost)
    winrate = computeWinRate(data)
    MDD     = computeMDD(data, cost)
    
    printFn('ROI', ROI)
    printFn('winrate', winrate)
    printFn('MDD', MDD)




