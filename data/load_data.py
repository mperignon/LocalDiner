import psycopg2

conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")



cur = conn.cursor()
cur.execute("""
CREATE TABLE venues(
    url text PRIMARY KEY,
    prediction float,
    count integer,
    lat float,
    lon float,
    name text,
    price integer,
    clean_address text,
    categories text,
    display_phone text,
    id text,
    rating float,
    review_count integer,
    cats text
)
""")
conn.commit()



with open('venues_with_locality_prediction.csv', 'r') as f:
    # Notice that we don't need the `csv` module.
    next(f)  # Skip the header row.
    cur.copy_from(f, 'venues', sep=',')
        
conn.commit()