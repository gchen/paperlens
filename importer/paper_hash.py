#ArNet

import MySQLdb
import sys
sys.path.append("../")
import hashlib
from paper import Paper

connection = MySQLdb.connect (host = "127.0.0.1", user = "paperlens", passwd = "paper1ens", db = "paperlens")
cursor = connection.cursor()

def intHash(buf):
    ret = 0
    for i in range(len(buf)):
        ret = ret * 31 + ord(buf[i])
    return ret % 200000000

try:
    cursor.execute("select id,title from paper")
    n = 0
    while 1:
        row = cursor.fetchone()
        if row == None:
            break
        paper_id = int(row[0])
        title = row[1]
        hash_value = intHash(title.lower())
        cursor.execute("update paper set hashvalue=%s where id=%s",(hash_value,paper_id))
        n = n + 1
        if n % 10000 == 0:
            print str(n)
    
    connection.commit()
    cursor.close()
    connection.close()
except MySQLdb.Error, e:
    print e.args[0], e.args[1]