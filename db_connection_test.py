import os
import psycopg2
from urllib import parse as urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse()

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

cursor = conn.cursor()
# data = [url[:-1],time.strftime('%Y-%m-%d %H:%M:%S'),channel_name]
# data_log = tuple(data)
# update_log=("INSERT INTO urls (url,shared_at,channel) VALUES (%s,%s,%s)")
cursor.execute("SELECT * FROM urls")

print (cursor.fetchall())
cursor.close()
