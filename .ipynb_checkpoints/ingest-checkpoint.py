import requests 
import psycopg2 

with requests.get("http://127.0.0.1:5000/very_large_request/100", stream=True) as r:

    conn = psycopg2.connect(dbname='postgres', 
                            user="postgres",
                            password="purun2005")
    cur = conn.cursor()
    sql = "INSERT INTO transactions (txid, uid, amount) VALUES (%s, %s, %s)"

    buffer = ""
    for chunk in r.iter_content(chunk_size=1):
        if chunk.endswith(b'\n'):
            t = eval(buffer)
            print(t)
            if t[2] > 900:
                print("**************you're a cool customer")
            cur.execute(sql, (t[0], t[1], t[2]))
            conn.commit()
            buffer = ""
        else:
            buffer += chunk.decode()