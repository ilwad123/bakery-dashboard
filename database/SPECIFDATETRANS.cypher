MATCH (t:Transaction)
WHERE date(datetime(t.Datetime)) = date("2023-12-07")
RETURN t