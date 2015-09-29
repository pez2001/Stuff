import sqlite3

c = sqlite3.connect('test.db')
cc = c.cursor()
cc.execute("CREATE TABLE test (date text, name text, money real)")
cc.execute("INSERT INTO test VALUES ('2012-06-02','pez',35.14)")
c.commit()
n = ("pez",)
cc.execute("SELECT * FROM test WHERE name=?", n)
print(cc.fetchone())

c.close()
