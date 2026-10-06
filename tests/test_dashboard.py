import pandas as pd
from holdings_tracker.dashboard import build_dashboard
def test_dashboard(tmp_path): assert build_dashboard(pd.DataFrame([{'value_usd':10}]),pd.DataFrame([{'action':'NEW'}]),tmp_path/'x.xlsx').exists()
