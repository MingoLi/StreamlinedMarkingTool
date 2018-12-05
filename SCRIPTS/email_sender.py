import smtplib
from configparser import ConfigParser, ExtendedInterpolation
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from config_reader import config_reader
from feedback import feedback
import re
import datetime

class email_sender:

    def __init__(self):
        self.EMAIL_LOG_NAME = 'email_log.ini'
        self.cr = config_reader()
        self.email_config = self.cr.get_email_settings()
        self.email_log_dir = self.cr.get_email_log()
        self.feedback = feedback()
        
    def verify_email_settings(self):
        EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

        if not EMAIL_REGEX.match(self.email_config.get('sendfrom')):
            print("Invalid email address: sendfrom, please check config.ini")
            return False

        # Check if the password has been change from the default one, or it's empty
        password = self.email_config.get('password')
        if 'Your Password' == password or not password:
            print("Please varify your password in config.ini")
            return False

        return True
 
    def send_email_not_in_use(self):
        # fromaddr = self.email_config.get('sendfrom')
        fromaddr = 'lim34521@myumanitoba.ca'
        toaddr = "liminghao0613@gmail.com"
        
        msg = MIMEMultipart()
        
        msg['From'] = fromaddr
        msg['To'] = toaddr
        # msg['Subject'] = self.email_config.get('subject')
        msg['Subject'] = 'Test msg'
        
        body = "TEXT YOU WANT TO SEND"
        
        msg.attach(MIMEText(body, 'plain'))
        
        # TODO: handle time out
        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(fromaddr, "Aa970613..")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        pass

    def construct_email_body(self, to):
        fd_list = self.feedback.get_feedback_of(to)
        full_mark = int(self.cr.get_rubrics().get('fullmark'))
        curr_mark = full_mark

        body = self.email_config.get('header')
        body += '\n=========================================\n\n'
        body += 'General\n-------------\n\n'
        for fd, mark in fd_list.items():
            body += fd + ': ' + mark + '\n'
            curr_mark += int(mark)
        body += '\n\n------\n\n'
        body += 'Grand total = ' + str(curr_mark) + '/' + str(full_mark)
        
        file_name = to + '.txt'
        file_path = self.cr.get_email_backup() + '/' + file_name
        with open(file_path, 'w+') as f:
            f.write(body)

        return body

    def log_write(self, to):
        log_path = self.email_log_dir + '/' + self.EMAIL_LOG_NAME
        parser = ConfigParser(interpolation=ExtendedInterpolation())
        parser.read(log_path)

        if not parser.has_section(to):
            parser.add_section(to)
            parser.set(to, 'timestamp', datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S"))
            parser.set(to, 'sendto', to+'@'+self.email_config.get('domain'))
            parser.set(to, 'subject', self.email_config.get('subject'))
            parser.set(to, 'email_body', to+'.txt')

            email_log = open(log_path, 'w+')
            parser.write(email_log)
            email_log.close()
        else:
            print('Warning: you may have sent a duplicated email to ' + to)
        pass
    
    def send_email_fake(self, to):
        if not self.verify_email_settings():
            return False

        self.construct_email_body(to)
        return True

    # Check whether this email has been sent 
    # True -> already sent
    def check_duplicate_from_log(self, to):
        log_path = self.email_log_dir + '/' + self.EMAIL_LOG_NAME
        parser = ConfigParser(interpolation=ExtendedInterpolation())
        parser.read(log_path)
        
        if parser.has_section(to):
            return True

        return False


    def send_email(self, to):
        if not self.verify_email_settings():
            return False

        if not self.check_duplicate_from_log(to):
            msg = MIMEText(self.construct_email_body(to))

            fromaddr = self.email_config.get('sendfrom')
            toaddr = to + '@' + self.email_config.get('domain')
            msg['Subject'] = self.email_config.get('subject')
            msg['From'] = fromaddr
            msg['To'] = toaddr

            smtp = self.email_config.get('smtp')
            port = self.email_config.get('port')
            password = self.email_config.get('password')

            # Send the message via our own SMTP server.
            try:
                server = smtplib.SMTP(smtp, port)
                server.starttls()
                server.login(fromaddr, password)
                server.send_message(msg)
                server.quit()

                self.log_write(to)
            except:
                print("Timeout, please check smtp settings and try again mannualy")

        return True

