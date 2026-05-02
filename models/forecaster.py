python3 << 'PYEOF'
code = '''
import numpy as np, pandas as pd, warnings
from datetime import datetime, timedelta
warnings.filterwarnings("ignore")
try:
    import xgboost as xgb
    from statsmodels.tsa.arima.model import ARIMA
    from sklearn.preprocessing import StandardScaler
    HAS_MODELS = True
except ImportError:
    HAS_MODELS = False

def _gen_history(n=120, base=82.0):
    np.random.seed(42)
    dates = [datetime.today() - timedelta(days=n-i) for i in range(n)]
    prices = [base]
    for _ in range(n-1):
        shock = np.random.normal(0, 1.2)
        drift = 0.05*(base - prices[-1])
        prices.append(max(prices[-1]+drift+shock, 40))
    return pd.DataFrame({"price": prices}, index=pd.to_datetime(dates))

def _features(df):
    df = df.copy()
    for lag in [1,3,7,14]: df[f"lag_{lag}"] = df["price"].shift(lag)
    df["rm7"]  = df["price"].rolling(7).mean()
    df["rs7"]  = df["price"].rolling(7).std()
    df["rm14"] = df["price"].rolling(14).mean()
    df["pct3"] = df["price"].pct_change(3)
    df["dow"]  = df.index.dayofweek
    return df.dropna()

FEAT = ["lag_1","lag_3","lag_7","lag_14","rm7","rs7","rm14","pct3","dow"]

class AegisForecaster:
    def __init__(self):
        self.arima = self.xgb = self.scaler = None
        self.hist = None
        self.fitted = False

    def fit(self, df=None):
        self.hist = df if df is not None else _gen_history()
        if not HAS_MODELS:
            self.fitted = True
            return self
        try:
            self.arima = ARIMA(self.hist["price"], order=(2,1,2)).fit()
        except:
            self.arima = None
        fd = _features(self.hist)
        X = fd[FEAT].values
        y = fd["price"].values
        self.scaler = StandardScaler()
        Xs = self.scaler.fit_transform(X)
        self.xgb = xgb.XGBRegressor(
            n_estimators=200, max_depth=4,
            learning_rate=0.05, subsample=0.8,
            colsample_bytree=0.8, random_state=42,
            verbosity=0
        ).fit(Xs, y)
        self.fitted = True
        print("Forecaster ready")
        return self

    def forecast(self, horizon_days=14, crisis_shock=0.0, disruption_factor=0.0):
        if not self.fitted:
            self.fit()
        base = float(self.hist["price"].iloc[-1])
        shocked = base*(1+crisis_shock/100)
        dates = [datetime.today()+timedelta(days=i+1) for i in range(horizon_days)]
        if self.arima:
            arima_p = list(self.arima.forecast(steps=horizon_days))
        else:
            arima_p = [base+np.random.normal(0,1)*(i+1)**0.5 for i in range(horizon_days)]
        rw = list(self.hist["price"].tail(14).values)
        if crisis_shock > 0:
            rw[-1] = shocked
        xgb_p = []
        for step in range(horizon_days):
            pw = rw[-14:]
            f = np.array([[pw[-1],pw[-3],pw[-7],pw[0],
                           np.mean(pw[-7:]),np.std(pw[-7:]),np.mean(pw),
                           (pw[-1]-pw[-4])/pw[-4] if pw[-4]!=0 else 0,
                           (datetime.today().weekday()+step+1)%7]])
            pred = float(self.xgb.predict(self.scaler.transform(f))[0])
            pred *= (1+disruption_factor*0.8*(1-step/horizon_days))
            xgb_p.append(pred)
            rw.append(pred)
        w = 0.7 if crisis_shock > 0 else 0.4
        prices = [round(w*xgb_p[i]+(1-w)*arima_p[i],2) for i in range(horizon_days)]
        std = float(self.hist["price"].pct_change().std())*base
        lower = [round(p-1.96*std*((i+1)**0.4),2) for i,p in enumerate(prices)]
        upper = [round(p+1.96*std*((i+1)**0.4),2) for i,p in enumerate(prices)]
        fp = prices[-1]
        pct = round((fp-base)/base*100,1)
        return {
            "base_price": round(base,2),
            "shocked_price": round(shocked,2),
            "horizon_days": horizon_days,
            "forecast": [{"date":d.strftime("%Y-%m-%d"),"price":p,"lower":l,"upper":u}
                         for d,p,l,u in zip(dates,prices,lower,upper)],
            "summary": {
                "final_price": fp, "pct_change": pct,
                "peak_price": round(max(prices),2),
                "peak_day": prices.index(max(prices))+1,
                "risk_score": min(100,round(abs(pct)*1.5+disruption_factor*40+(crisis_shock/100)*30,1)),
                "delay_prob": min(99,round(disruption_factor*65+(pct/100)*20,1)),
                "cost_impact": round(pct*0.35+disruption_factor*18,1),
            },
            "model": "ARIMA+XGBoost hybrid",
        }

_fc = None
def get_forecaster():
    global _fc
    if _fc is None:
        _fc = AegisForecaster().fit()
    return _fc
'''
with open("/opt/aegis/models/forecaster.py","w") as f:
    f.write(code)
print("forecaster.py written OK")
PYEOF

✅ Should print: forecaster.py written OK
