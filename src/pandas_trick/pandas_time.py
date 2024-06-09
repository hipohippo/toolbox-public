import pandas as pd

d = pd.Period("2020-3", freq="D")
d += 1

drange = pd.period_range("2021-01-01", "2021-03-01", freq="5D")
wrange = pd.period_range("2021-01-01", "2021-03-01", freq="3W")
mrange = pd.period_range("2021-01-01", "2021-03-01", freq="1M")
hrange = pd.period_range("2021-01-01", "2021-03-01", freq="12H")  # type(hrange[0]) == Period

pd.date_range("2021-01-01", "2021-05-01", freq="12H")
pd.date_range("2021-01-01", "2021-01-02", periods=25)  ## 25 sample points


pd.Timestamp.now().normalize()
pd.Timedelta("3 min").components.minutes #?