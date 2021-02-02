import smtplib
conn = smtplib.SMTP('imap.gmail.com',587)
conn.ehlo()
conn.starttls()
conn.login('', '')

conn.sendmail('arthurpdesimone@gmail.com','arthurpdesimone@gmail.com','Subject: What you like? \n\n Reply Reply Reply')
conn.quit()