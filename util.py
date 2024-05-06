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