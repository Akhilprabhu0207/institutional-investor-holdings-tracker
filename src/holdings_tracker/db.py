from contextlib import contextmanager
import os
class Database:
    def __init__(self,dsn=None): self.dsn=dsn or os.environ['DATABASE_URL']
    @contextmanager
    def connect(self):
        import psycopg
        with psycopg.connect(self.dsn) as conn: yield conn
    def save(self,filing,filer_name,holdings):
        with self.connect() as conn,conn.cursor() as cur:
            cur.execute('INSERT INTO filers(cik,name) VALUES (%s,%s) ON CONFLICT(cik) DO UPDATE SET name=EXCLUDED.name, updated_at=now()',(filing.cik,filer_name))
            cur.execute('INSERT INTO filings(accession,cik,form_type,filed_date,report_period,is_amendment,primary_document,information_table_document,source_url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT(accession) DO UPDATE SET information_table_document=EXCLUDED.information_table_document',(filing.accession,filing.cik,filing.form_type,filing.filed_date,filing.report_period,filing.form_type.endswith('/A'),filing.primary_document,filing.information_table_document,filing.source_url))
            for h in holdings: cur.execute('INSERT INTO holdings(accession,row_number,name_of_issuer,title_of_class,cusip,figi,value_usd,shares_or_principal,shares_type,put_call,investment_discretion,other_manager,voting_sole,voting_shared,voting_none) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT(accession,row_number) DO UPDATE SET value_usd=EXCLUDED.value_usd, shares_or_principal=EXCLUDED.shares_or_principal',(filing.accession,h.row_number,h.name_of_issuer,h.title_of_class,h.cusip,h.figi,h.value_usd,h.shares_or_principal,h.shares_type,h.put_call,h.investment_discretion,h.other_manager,h.voting_sole,h.voting_shared,h.voting_none))
