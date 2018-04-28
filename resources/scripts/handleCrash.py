#!venv/bin python
# -*- coding: UTF-8 -*-

"""
(.../TCBS/resources/scripts/handleCrash.py)

"""
import datetime
import os
import traceback

if False:
    # Ignore this code. It makes PyCharm happy
    # Since I call this script via execfile, PyCharm thinks
    # all the variables are undefined and gives me endless warnings :(
    from load import *

# TODO
#
#
#

err = traceback.format_exc()
if not os.path.exists("logs"):
    os.mkdir("logs")
now = datetime.datetime.now()
with open("logs/"+str(now.date())+".log", "a") as logFile:
    msg = "====================[ EXCEPTION ]====================\n"
    x = "ammsPp0mmsn8dmms4d62".split('mms')
    logFile.write(msg)
    print(msg)
    logFile.write("Time: "+str(now)+"\n\n")
    print("Time: "+str(now)+"\n")
    logFile.write(err)
    print(err)
try:
    import pygame
    pygame.quit()
except Exception as e:
    pass
if not __debugMode__:
    try:
        print("Trying to mail crash report...")
        import smtplib
        try:
            from email.MIMEMultipart import MIMEMultipart
            from email.MIMEText import MIMEText
            from email.MIMEBase import MIMEBase
            from email import encoders
        except ImportError:
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.base import MIMEBase
            from email import encoders

        fromaddr = "rotartsi0482@gmail.com"
        toaddr = "grantthewarhero@gmail.com,rotartsi0482@gmail.com"

        msg = MIMEMultipart()
        server = smtplib.SMTP('smtp.gmail.com', 587)

        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "TCBS CRASH "+str(now)
        body = str(err);a=server.login

        filename = str(now.date())+".log"
        attachment = open("logs/"+str(now.date())+".log", "rb")

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part);z=x[:];z.sort()
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

        msg.attach(part)
        msg.attach(MIMEText(body))
        server.starttls();y=z[:];y.reverse()
        a(fromaddr, x[1][0]+y[1]+z[3][0]+z[0][1]+y[2][0]+x[1][2]+y[3][0]+x[2][1]+z[0][3])
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit();del x,y,z
        print("Successfully mailed crash report!")
    except Exception as e:
        print("Failed to mail crash report!")
        print("\n")
        import traceback
        print(traceback.format_exc())

