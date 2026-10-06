import argparse,os
from pathlib import Path
import pandas as pd
from .dashboard import build_dashboard
from .parser import parse_information_table
from .sec_client import SECClient
from .db import Database
def main():
 p=argparse.ArgumentParser(); p.add_argument('--cik',required=True); p.add_argument('--quarters',type=int,default=1); p.add_argument('--xml'); p.add_argument('--accession'); p.add_argument('--filer-name',default='Local sample'); p.add_argument('--output-dir',default='data/raw'); p.add_argument('--dashboard'); p.add_argument('--load-db',action='store_true'); a=p.parse_args()
 if a.xml:
  h=parse_information_table(a.xml); df=pd.DataFrame([x.__dict__ for x in h]);
  if a.dashboard: build_dashboard(df,pd.DataFrame(),a.dashboard)
  print(f'Parsed {len(h)} holdings from {a.xml}'); return
 c=SECClient(os.environ['SEC_USER_AGENT']); filings=c.recent_13f(a.cik,a.quarters); rows=[]
 for f in filings:
  f=c.resolve_information_table(f); xml=c.download_xml(f); out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True); (out/f'{f.accession}.xml').write_bytes(xml); hs=parse_information_table(xml)
  if a.load_db: Database().save(f,a.filer_name,hs)
  rows += [{'cik':f.cik,'accession':f.accession,'report_period':f.report_period,**h.__dict__} for h in hs]
 df=pd.DataFrame(rows); build_dashboard(df,pd.DataFrame(),a.dashboard) if a.dashboard else None
 print(f'Downloaded and parsed {len(filings)} filing(s), {len(rows)} holding rows.')
if __name__=='__main__': main()
