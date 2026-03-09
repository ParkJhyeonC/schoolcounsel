from app.services import monthly_approval_ledger, parse_nice_csv, student_card


def test_parse_and_ledger_and_card():
    raw = b"date,student_id,student_name,grade,class_name,counselor,topic,method,duration_minutes,notes\n2026-03-01,1,A,1,1,T,Topic,ind,20,n\n2026-03-01,2,B,1,1,T,Topic2,grp,30,n2\n"
    records = parse_nice_csv(raw)
    assert len(records) == 2

    ledger = monthly_approval_ledger(records, "2026-03")
    assert ledger[0]["count"] == 2
    assert ledger[0]["total_minutes"] == 50

    card = student_card(records, "1")
    assert card["student_name"] == "A"
