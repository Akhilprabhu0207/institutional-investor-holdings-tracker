from dataclasses import dataclass
from datetime import date
import requests
SEC_BASE='https://data.sec.gov'; ARCHIVES='https://www.sec.gov/Archives/edgar/data'
@dataclass(frozen=True)
class Filing: accession:str; cik:str; form_type:str; filed_date:date; report_period:date; primary_document:str; information_table_document:str; source_url:str
class SECClient:
 def __init__(self,user_agent,timeout=30):
  if not user_agent or '@' not in user_agent: raise ValueError('SEC_USER_AGENT must include an email address')
  self.session=requests.Session(); self.session.headers.update({'User-Agent':user_agent,'Accept-Encoding':'gzip, deflate'}); self.timeout=timeout
 def _get_json(self,url): r=self.session.get(url,timeout=self.timeout); r.raise_for_status(); return r.json()
 def submissions(self,cik): return self._get_json(f'{SEC_BASE}/submissions/CIK{int(cik):010d}.json')
 def recent_13f(self,cik,limit=4):
  recent=self.submissions(cik)['filings']['recent']; found=[]
  for i,form in enumerate(recent['form']):
   if form not in ('13F-HR','13F-HR/A') or not recent['reportDate'][i]: continue
   a=recent['accessionNumber'][i]; found.append(Filing(a,f'{int(cik):010d}',form,date.fromisoformat(recent['filingDate'][i]),date.fromisoformat(recent['reportDate'][i]),recent['primaryDocument'][i],'',f'{ARCHIVES}/{int(cik)}/{a.replace("-","")}/'))
   if len(found)>=limit: break
  return found
 def resolve_information_table(self,filing):
  d=self._get_json(f'{ARCHIVES}/{int(filing.cik)}/{filing.accession.replace("-","")}/index.json'); names=[x['name'] for x in d.get('directory',{}).get('item',[])]; xmls=[n for n in names if n.lower().endswith('.xml')]; candidates=[n for n in xmls if 'table' in n.lower() or '13f' in n.lower()]; info=candidates[0] if candidates else next((n for n in xmls if n!=filing.primary_document),None)
  if not info: raise FileNotFoundError(f'No information-table XML found for {filing.accession}')
  return Filing(**{**filing.__dict__,'information_table_document':info})
 def download_xml(self,filing):
  if not filing.information_table_document: filing=self.resolve_information_table(filing)
  r=self.session.get(f'{ARCHIVES}/{int(filing.cik)}/{filing.accession.replace("-","")}/{filing.information_table_document}',timeout=self.timeout); r.raise_for_status(); return r.content
