import argparse,os
from pathlib import Path
import pandas as pd
from .dashboard import build_dashboard
from .parser import parse_information_table
from .sec_client import SECClient
from .db import Database
def main():
    p=argparse.ArgumentParser(description='Ingest SEC 13F information tables'); p.add_argument('--cik',required=True); p.add_argument('--quarters',type=int,default=1); p.add_argument('--xml'); p.add_argument('--accession'); p.add_argument('--filer-name',default='Local sample'); p.add_argument('--output-dir',default='data/raw'); p.add_argument('--dashboard'); p.add_argument('--load-db',action='store_true'); a=p.parse_args()
    if a.xml:
        holdings=parse_information_table(a.xml); hdf=pd.DataFrame([h.__dict__ for h in holdings]); qdf=pd.DataFrame();
        if a.dashboard: build_dashboard(hdf,qdf,a.dashboard)
        print(f'Parsed {len(holdings)} holdings from {a.xml}'); return
    client=SECClient(os.environ['SEC_USER_AGENT']); filings=client.recent_13f(a.cik,a.quarters); rows=[]
    for filing in filings:
        filing=client.resolve_information_table(filing); xml=client.download_xml(filing); out=Path(a.output_dir); out.mkdir(parents=True,exist_ok=True); (out/f'{filing.accession}.xml').write_bytes(xml); holdings=parse_information_table(xml)
        if a.load_db: Database().save(filing,a.filer_name,holdings)
        for h in holdings: rows.append({'cik':filing.cik,'accession':filing.accession,'report_period':filing.report_period,**h.__dict__})
    hdf=pd.DataFrame(rows); qdf=pd.DataFrame();
    if a.dashboard: build_dashboard(hdf,qdf,a.dashboard)
    print(f'Downloaded and parsed {len(filings)} filing(s), {len(rows)} holding rows.'+(' Loaded into PostgreSQL.' if a.load_db else ''))
if __name__=='__main__': main()
