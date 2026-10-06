from decimal import Decimal
from pathlib import Path
from holdings_tracker.parser import parse_information_table
def test_parse_sample():
    rows=parse_information_table(Path('examples/sample_13f.xml')); assert len(rows)==2; assert rows[0].name_of_issuer=='ACME CORP'; assert rows[0].cusip=='000000101'; assert rows[0].value_usd==1250000; assert rows[0].shares_or_principal==Decimal('125000'); assert rows[1].investment_discretion=='DFND'
def test_namespace_prefix_does_not_matter():
    xml='<informationTable xmlns="x"><infoTable><nameOfIssuer>A</nameOfIssuer><value>1</value><shrsOrPrnAmt><sshPrnamt>2</sshPrnamt></shrsOrPrnAmt></infoTable></informationTable>'; assert parse_information_table(xml)[0].name_of_issuer=='A'
