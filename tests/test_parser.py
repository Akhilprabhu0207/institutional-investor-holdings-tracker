from decimal import Decimal
from pathlib import Path
from holdings_tracker.parser import parse_information_table
def test_parse_sample():
 r=parse_information_table(Path('examples/sample_13f.xml')); assert len(r)==2; assert r[0].name_of_issuer=='ACME CORP'; assert r[0].shares_or_principal==Decimal('125000')
def test_namespace_prefix_does_not_matter(): assert parse_information_table('<informationTable xmlns="x"><infoTable><nameOfIssuer>A</nameOfIssuer><value>1</value><shrsOrPrnAmt><sshPrnamt>2</sshPrnamt></shrsOrPrnAmt></infoTable></informationTable>')[0].name_of_issuer=='A'
