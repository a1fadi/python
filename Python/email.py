from email.message import EmailMessage
from src.data_store import data_store
import smtplib

def compose_email(email, reset_code):
    user = data_store.get()['users']
    i = 0
    while (email != user[i]['email']):
        i += 1
    name = user[i]['name_first']
    gmail_user = 'f09a.ant.test@gmail.com'
    gmail_password = 'Password!23'

    sent_from = gmail_user
    to = [email]
    
    subject = "UNSW Stream reset password"

    plain_text = f""" To {name} ,
    
    Your code to reset your password is {reset_code} and you have been logged out of all active sessions on UNSW streams. 
    If you did not request a password reset please disregard this email.
    
    Have a wonderful day!
    -The UNSW streams team"""
    
    msg = EmailMessage()
    msg.set_content(plain_text) 
    msg['Subject'] = subject
    msg['From'] = sent_from
    msg['To'] = ','.join(to)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.send_message(msg)
    server.close()
    
    return