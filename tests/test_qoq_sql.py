from pathlib import Path
def test_qoq_query_prefers_amendments():
    sql=Path('sql/qoq_changes.sql').read_text(); assert 'ORDER BY f.is_amendment DESC' in sql; assert 'PARTITION BY f.cik, f.report_period' in sql; assert "WHEN shares_or_principal = 0 THEN 'SOLD_OUT'" in sql
