import smtplib
def sendgmail():
    to = 'mazaoa@hotmail.com'
    gmail_user = 'chan.teerapon@gmail.com'
    gmail_pwd = '08888******'
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    import pdb; pdb.set_trace()
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(gmail_user, gmail_pwd)
    header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:testing \n'
    print header
    msg = header + '\n this is test msg from mkyong.com \n\n'
    smtpserver.sendmail(gmail_user, to, msg)
    print 'done!'
    smtpserver.close()
    sendgmail()
