#! /usr/bin/python

import smtplib
from email.mime.text import MIMEText

SERVER =    'simac-gmbh.de'
PORT =      587
EMAIL =    ''
PASSWORT =  'xxx' 
EMPFAENGER =    ['j.ciszewski@simac-gmbh.de']
SUBJECT =   'Raspberry Pi STROMAUSFALL!'
BODY =      """
<html>
 <head></head>
  <body>

<style type="text/css">
.tg  {border-collapse:collapse;border-spacing:0;}
.tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
.tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
.tg .tg-0ord{text-align:right}
.tg .tg-qnmb{font-weight:bold;font-size:16px;text-align:center}
</style>
<table class="tg">
  <tr>
    <th class="tg-qnmb" colspan="2">StromPi hat einen STROMAUSFALL erkannt!!!!</th>
  </tr>
</table>
  </body>
</html>
"""

session = smtplib.SMTP(SERVER, PORT)
session.set_debuglevel(1)
session.ehlo()
session.starttls()
session.ehlo
session.login(EMAIL, PASSWORT)
msg = MIMEText(BODY, 'html')
msg['Subject'] = SUBJECT
msg['From'] = EMAIL
msg['To'] = ", ".join(EMPFAENGER)
session.sendmail(EMAIL, EMPFAENGER, msg.as_string())
session.quit()
