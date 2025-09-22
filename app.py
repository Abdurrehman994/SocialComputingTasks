import sqlite3

database_path = 'database.sqlite'
conn=sqlite3.connect(database_path)
c=conn.cursor()

c.execute('Select name from sqlite_master where type= "table"')
tables=c.fetchall()
print("Tables in the database:", tables)  
 

# Task 1.1:

for table_name in tables:
    table_name = table_name[0]
    c.execute('PRAGMA table_info({})'.format(table_name))
    columns=c.fetchall()
    print("\nColumns in table '{}':".format(table_name), columns)
    c.execute('Select count(*) from {}'.format(table_name))
    count=c.fetchone()[0]
    print("Number of records in table '{}': {}".format(table_name, count))


# Task 1.2
c.execute("Select count(*) from users u where u.id not in (Select user_id from posts)" \
"and u.id not in (Select user_id from reactions)")
Lurkers_users_count=c.fetchone()[0]
print("\nNumber of lurkers:", Lurkers_users_count)


# Task 1.3

c.execute("select u.id,u.username,count(r.id) as reaction_count from users u " \
          "left join reactions r on u.id=r.user_id " \
            "group by u.id " \
                "order by reaction_count desc " \
                "limit 5")
top_5_users=c.fetchall()
print("\nTop 5 users by reactions made:")  
for user in top_5_users:
    print(user)

# Task 1.4
c.execute("select u.id,u.username,c.text,count(*) as repeat_count from" \
          "(select user_id,content as text from comments union all select user_id,content as text from posts) c " \
            "join users u on c.user_id=u.id " \
                "group by u.id,u.username, c.text " \
                "having count(*)>=3 " \
                "order by repeat_count desc")
spammers=c.fetchall()
print("\nUsers with repeated content (3 or more times):")
for spammer in spammers:
    print(spammer)
          
conn.close()


