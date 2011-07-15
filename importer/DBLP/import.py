import MySQLdb
import sys
sys.path.append("../")
from paper import Paper

def Extrack(buf):
    p1 = buf.find('>')
    key = ''
    value = ''
    p1 = p1 + 1
    p2 = buf.find('<', p1)
    key = buf[0:p1]
    value = buf[p1:p2]
    return [key,value]

connection = MySQLdb.connect (host = "127.0.0.1", user = "paperlens", passwd = "paper1ens", db = "paperlens")
cursor = connection.cursor()

data = open("../../../data/dblp.xml")

item = Paper()

try:
    for line in data:
        if line.find('<incollection') >= 0:
            item = Paper()
        elif line.find('</incollection>') >= 0:
            print "insert into paper(title,year,booktitle) values (\'" + item.title, "\', " + str(item.publish_year) + ", \'" + item.booktitle + "\');"
            cursor.execute("insert into paper(title,year,booktitle) values (\'" + item.title, "\', " + str(item.publish_year) + ", \'" + item.booktitle + "\');")
            conn.commit()
            item = Paper()
        else:
            [key,value] = Extrack(line)
            if key == "<author>":
                item.authors.append(value)
            elif key == "<title>":
                item.title = value.strip('.')
            elif key == "<year>":
                item.publish_year = int(value)
            elif key == "<booktitle>":
                item.booktitle = value

    cursor.close()
    connection.close()
except MySQLdb.Error, e:
    print e.args[0], e.args[0]
