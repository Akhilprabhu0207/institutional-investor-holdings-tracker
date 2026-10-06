import pandas as pd
from holdings_tracker.dashboard import build_dashboard
def test_dashboard(tmp_path):
    out=build_dashboard(pd.DataFrame([{'name_of_issuer':'A','value_usd':10}]),pd.DataFrame([{'action':'NEW'}]),tmp_path/'x.xlsx'); assert out.exists()
