


__author__ = 'franciscosauceda'



import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pymysql
import os
import HTML
import pandas as ps


os.chdir('to/specific/folder')

conn = pymysql.connect(host='db.example.com', port=3306, user='user_name', passwd='password', db='optional')

cur = conn.cursor()

#mysql querry
query = ("""query_example_here""")

#executes the query
cur.execute(query)

#turns tuple query into string
rows = cur.fetchall()

new_rows = []
for i,row in enumerate(rows):
    col_list = []
    for j,col in enumerate(row):
        if col == 0:
            col = '0'
        col_list.append(col)
    new_rows.append(col_list)


#dumps MySQL query into datafram
df = ps.DataFrame(new_rows)

#rearanges columns so tech operator is first
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]

#relabels the columns
df.columns = ['column_1', 'column_2']

#converts dataframe to HTML table
data = ps.DataFrame.to_html(df, justify= 'Center', index= False)

# me == my email address
# you == recipient's email address
me = "me@gmail.com"
you = "you@gmail.com"

# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Weekly Tech Support Report"
msg['From'] = me
msg['To'] = you

# Create the body of the message (a plain-text and an HTML version).
text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
html = 'Happy Monday morning! This is your weekly NPS/tech support report whipped up fresh by yours truly, Francisco Sauceda. This report details the number of detractor scores per surverys taken. Enjoy!'  + data

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)

# Send the message via local SMTP server.

mail = smtplib.SMTP('smtp.gmail.com', 587)

mail.ehlo()

mail.starttls()

mail.login('user_name@gmail.com', 'password')
mail.sendmail(me, you ,msg.as_string())
mail.quit()