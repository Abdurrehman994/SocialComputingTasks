import sqlite3
import matplotlib.pyplot as plt

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

c.execute("select u.id,u.username,count(r.id) + count(cm.id) as reaction_count from users u " \
          "join posts p on u.id=p.user_id " \
          "left join reactions r on p.id=r.post_id " \
            "left join comments cm on p.id=cm.post_id " \
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

"==================Exercise 2==================="
# Task 2.1
c.execute("select substr(created_at,1,4) as year, count(*) from posts " \
          "group by year " \
          "order by year")
annual_posts=c.fetchall()
total_years = [int(row[0]) for row in annual_posts]
post_counts = [row[1] for row in annual_posts]
plt.plot(total_years, post_counts, marker='o')
plt.title('Number of Posts Per Year')
plt.xlabel('Year')
plt.ylabel('Number of Posts')
plt.grid()
plt.show()
# Calculating growth rate
initial_posts = post_counts[0]
final_posts = post_counts[-1]
num_years = total_years[-1] - total_years[0]
growth_rate = (final_posts / initial_posts) ** (1 / num_years) - 1
renting_servers = 16
years_to_plan = 3
future_posts = final_posts * ((1 + growth_rate) ** years_to_plan)
required_servers = future_posts / final_posts * renting_servers * 1.2
print("Estimated number of servers needed to rent based on past growth trends:", int(required_servers))

# Task 2.2
c.execute("select p.id, p.content, (count(distinct r.id) + count(distinct cm.id)) as virality_score " \
          "from posts p " \
          "left join reactions r on p.id=r.post_id " \
          "left join comments cm on p.id=cm.post_id " \
          "group by p.id " \
          "order by virality_score desc " \
          "limit 3")

top3_viral_posts=c.fetchall()
print("\nTop 3 viral posts based on reactions and comments:")
for post in top3_viral_posts:
    print(post) 

# task 2.3
c.execute("SELECT p.id, p.created_at, "
          "MIN(e.engagement_time) AS first_reaction_time, "
          "MAX(e.engagement_time) AS last_reaction_time, "
          "JULIANDAY(MIN(e.engagement_time)) - JULIANDAY(p.created_at) AS time_to_first_reaction, "
          "JULIANDAY(MAX(e.engagement_time)) - JULIANDAY(p.created_at) AS time_to_last_reaction "
          "FROM posts p "
          "LEFT JOIN ( "
          "  SELECT post_id, created_at AS engagement_time FROM reactions "
          "  UNION ALL "
          "  SELECT post_id, created_at AS engagement_time FROM comments "
          ") e ON p.id = e.post_id "
          "GROUP BY p.id")


#task 2.4
c.execute("select CASE WHEN e.user_id < p.user_id THEN e.user_id ELSE p.user_id END AS user1, " \
          "CASE WHEN e.user_id > p.user_id THEN e.user_id ELSE p.user_id END AS user2, " \
            "count(*) as interaction_count " \
            "from posts p " \
            "join ( " \
              "select user_id,post_id from reactions " \
              "union all " \
              "select user_id,post_id from comments " \
            ") e on p.id=e.post_id " \
            "where e.user_id != p.user_id " \
            "group by user1,user2 " \
            "order by interaction_count desc" \
                " limit 3")
top3_user_interactions=c.fetchall()
print("\nTop 3 user pairs with most interactions:")
for interaction in top3_user_interactions[:3]:
    print(interaction)







conn.close()


