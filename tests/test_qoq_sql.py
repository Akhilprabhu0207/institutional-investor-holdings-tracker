from pathlib import Path
def test_qoq_query_prefers_amendments():
 s=Path('sql/qoq_changes.sql').read_text(); assert 'ORDER BY f.is_amendment DESC' in s; assert 'PARTITION BY f.cik,f.report_period' in s; assert "WHEN shares_or_principal=0 THEN 'SOLD_OUT'" in s
