import darts.datasets
import pandas as pd

dataset_names = [
    'AirPassengersDataset', 
    'AusBeerDataset', 
    'AustralianTourismDataset', 
    'ETTh1Dataset', 
    'ETTh2Dataset', 
    'ETTm1Dataset', 
    'ETTm2Dataset', 
    'ElectricityDataset', 
    'EnergyDataset', 
    'ExchangeRateDataset', 
    'GasRateCO2Dataset', 
    'HeartRateDataset', 
    'ILINetDataset', 
    'IceCreamHeaterDataset', 
    'MonthlyMilkDataset', 
    'MonthlyMilkIncompleteDataset', 
    'SunspotsDataset', 
    'TaylorDataset', 
    'TemperatureDataset',
    'TrafficDataset', 
    'USGasolineDataset', 
    'UberTLCDataset', 
    'WeatherDataset', 
    'WineDataset', 
    'WoolyDataset',
]

def get_descriptions(w_references=False):
    descriptions = []
    for dsname in dataset_names:
        d = getattr(darts.datasets,dsname)().__doc__
        
        if w_references:
            descriptions.append(d)
            continue

        lines = []
        for l in d.split("\n"):
            if l.strip().startswith("References"):
                break
            if l.strip().startswith("Source"):
                break
            if l.strip().startswith("Obtained"):
                break
            lines.append(l)
        
        d = " ".join([x.strip() for x in lines]).strip()

        descriptions.append(d)

    return dict(zip(dataset_names,descriptions))
#如果是ILI用这个
def get_dataset1(dsname):
    #这个会出现哈希检验报错
    #darts_ds = getattr(darts.datasets,dsname)().load()
    print("DS_NAME",dsname)
    #dataset_file_path = f"/nethome/hliu763/.darts/datasets/ILINet.csv"  # 替换为实际路径
    
    dataset_file_path = f"/nethome/hliu763/ILINet-1oyNew.csv"
    dataset_file_path = f"/nethome/hliu763/ILINet23.csv"
    #dataset_file_path = f"/nethome/hliu763/reformatted_ILINet.csv"
    # 使用 pandas 直接读取 CSV 文件
    darts_ds = pd.read_csv(dataset_file_path)
    #print(darts_ds.columns)  # 打印所有列名

    if dsname=='GasRateCO2Dataset':
        darts_ds = darts_ds[darts_ds.columns[1]]
    if dsname == 'ILINetDataset':
        # 假设 ILINetDataset 的数据也在第二列，根据实际情况调整
        series = darts_ds[darts_ds.columns[1]]
        # series = darts_ds.pd_series()
        #series = darts_ds['Y']
    return series
def get_datasets1(n=-1,testfrac=0.2):
    datasets = [
        'ILINetDataset'#我自己加的
    ]
    datas = []
    for i,dsname in enumerate(datasets):
        series = get_dataset(dsname)
        splitpoint = int(len(series)*(1-testfrac))
        #splitpoint改为0
        splitpoint=20
        train = series.iloc[:splitpoint]
        test = series.iloc[splitpoint:]
        datas.append((train,test))
        if i+1==n:
            break
    return dict(zip(datasets,datas))
def get_dataset(dsname):
    darts_ds = getattr(darts.datasets,dsname)().load()
    if dsname=='GasRateCO2Dataset':
        darts_ds = darts_ds[darts_ds.columns[1]]
    series = darts_ds.pd_series()

    if dsname == 'SunspotsDataset':
        series = series.iloc[::4]
    if dsname =='HeartRateDataset':
        series = series.iloc[::2]
    return series
def get_datasets(n=-1,testfrac=0.2):
    datasets = [
        'AirPassengersDataset',
        'AusBeerDataset',
        'GasRateCO2Dataset', # multivariate
        'MonthlyMilkDataset',
        'SunspotsDataset', #very big, need to subsample?
        'WineDataset',
        'WoolyDataset',
        'HeartRateDataset',
    ]
    datas = []
    for i,dsname in enumerate(datasets):
        series = get_dataset(dsname)
        splitpoint = int(len(series)*(1-testfrac))
        
        train = series.iloc[:splitpoint]
        test = series.iloc[splitpoint:]
        datas.append((train,test))
        if i+1==n:
            break
    return dict(zip(datasets,datas))

def get_memorization_datasets(n=-1,testfrac=0.15, predict_steps=30):
    datasets = [
        'IstanbulTraffic',
        'TSMCStock',
        'TurkeyPower'
    ]
    datas = []
    for i,dsname in enumerate(datasets):
        with open(f"datasets/memorization/{dsname}.csv") as f:
            series = pd.read_csv(f, index_col=0, parse_dates=True).values.reshape(-1)
            # treat as float
            series = series.astype(float)
            series = pd.Series(series)
        if predict_steps is not None:
            splitpoint = len(series)-predict_steps
        else:    
            splitpoint = int(len(series)*(1-testfrac))
        train = series.iloc[:splitpoint]
        test = series.iloc[splitpoint:]
        datas.append((train,test))
        if i+1==n:
            break
    return dict(zip(datasets,datas))