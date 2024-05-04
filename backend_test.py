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

def computeROI (data:list, cost:float):
    netProfit = 0
    
    for trade in data:
        netProfit += trade['fee']
        netProfit += trade['fillPnl']

    return netProfit / cost * 100

def loadData(path:str):
    with open(path) as json_file: 
        rawData = json.load(json_file)
        
        code = rawData["code"]
        msg  = rawData["msg"]
        data = rawData["data"]
    return code, msg, data
        
        
        
if __name__ == '__main__':
    code, msg, data = loadData('trades.json')
    
    cost = 8000
    data = preprocess(data)

    ROI = computeROI(data, cost)
    
    print('ROI:', f'{ROI}%')    



