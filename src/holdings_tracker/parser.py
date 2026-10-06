from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
import xml.etree.ElementTree as ET
@dataclass(frozen=True)
class Holding:
    row_number:int; name_of_issuer:str; title_of_class:str|None; cusip:str|None; figi:str|None; value_usd:int; shares_or_principal:Decimal; shares_type:str|None; put_call:str|None; investment_discretion:str|None; other_manager:str|None; voting_sole:Decimal|None; voting_shared:Decimal|None; voting_none:Decimal|None
def _local(tag:str)->str: return tag.rsplit('}',1)[-1]
def _children(node): return {_local(c.tag):c for c in node}
def _text(node,key):
    child=_children(node).get(key); return child.text.strip() if child is not None and child.text else None
def _decimal(value): return Decimal(value) if value not in (None,'') else None
def parse_information_table(xml_bytes):
    if isinstance(xml_bytes,(str,Path)) and Path(str(xml_bytes)).exists(): root=ET.parse(xml_bytes).getroot()
    else: root=ET.fromstring(xml_bytes)
    rows=[n for n in root.iter() if _local(n.tag)=='infoTable']; out=[]
    for i,row in enumerate(rows,1):
        shares=_children(row).get('shrsOrPrnAmt'); voting=_children(row).get('votingAuthority'); sm=_children(shares) if shares is not None else {}
        out.append(Holding(i,_text(row,'nameOfIssuer') or '',_text(row,'titleOfClass'),_text(row,'cusip'),_text(row,'FIGI'),int(_text(row,'value') or 0),Decimal(sm.get('sshPrnamt').text) if sm.get('sshPrnamt') is not None else Decimal(0),_text(shares,'sshPrnamtType') if shares is not None else None,_text(row,'putCall'),_text(row,'investmentDiscretion'),_text(row,'otherManager'),_decimal(_text(voting,'Sole')) if voting is not None else None,_decimal(_text(voting,'Shared')) if voting is not None else None,_decimal(_text(voting,'None')) if voting is not None else None))
    return out
