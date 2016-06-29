
#!/bin/env ./venv/bin/python3.5
import lxml.html as s
import requests as r
import MySQLdb
import re
import time

db = MySQLdb.connect("172.5.25.7", "user", "change_me", "db")
for i in range(1, 1400):
    # Be nice and don't DOS the site:
    time.sleep(.2)

    page = r.get('http://localhost/bla/page.php?songId={}'.format(i))
    tree = s.fromstring(page.content)

    song = tree.xpath('//font[@size="+5"]/text()')
    artist = tree.xpath('//font[@size="+2"]/text()')
    facts = tree.xpath('//table[@width="60%"]/tr/td/text()')
    if artist:
        # Some escaping to "
        artist=artist[0].replace("'","\"")
        song=song[0].replace("'","\"")

        sql = "INSERT INTO mima.facts_artist (`name`) VALUES ('{!s}') " \
              "ON DUPLICATE KEY UPDATE `name`='{!s}' ".format(artist, artist)

        cursor = db.cursor()
        cursor.execute(sql)
        # Could use try/catch here. (a  TODO later

        db.commit()

        cursor.execute("select id from mima.facts_artist WHERE name='{}'".format(artist))
        # execute doesn't return the Insert ID afaik so ... lets grab it
        arid = cursor.fetchone()[0]
        sql = "INSERT INTO mima.facts_song (`name`,`artist_id` ) VALUES ('{song:s}' , {arid:d}) " \
              "ON DUPLICATE KEY UPDATE `name`='{song:s}' ".format(song=song, arid=arid)

        cursor.execute(sql) #try catch bla bla ..
        db.commit()
        cursor.execute("select id from mima.facts_artist WHERE name='{}'".format(artist))
        soid = cursor.fetchone()[0]
        for f in facts:
            if re.search('[א-ת]' , f):

                f = f.replace("'","\"")
                f = f.replace("\n"," ")
                f = f.replace("\r"," ")

                sql = "INSERT INTO mima.facts_fact (`content`,`song_id` ) VALUES ('{f:s}' , {soid:d}) " \
                     "ON DUPLICATE KEY UPDATE `content`='{f:s}' ".format(f=f, soid=soid)
                cursor.execute(sql)
                db.commit()

db.close()
