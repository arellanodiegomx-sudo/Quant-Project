import psycopg2
from datetime import datetime

# connection function
def get_connection():
    conn = psycopg2.connect(
        dbname = "quant_db",
        user = "diegoarellano",
        password = "",
        host = "localhost",
        #port not needed if using default port 5432
    )
    return conn

def save_price(ticker: str, price: float):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO prices (ticker, price) VALUES (%s, %s)", (ticker, price) #prevents SQL injection use %s and tuple
    )

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Saved {ticker}: ${price:.2f} to database at {datetime.now()}")



