#!/usr/bin/env python
import poplib
import os
import sys
import logging
import time
from email.parser import Parser
from getpass import getpass
from optparse import OptionParser

def get_password():
    if sys.stdin.isatty():
        return getpass("POP3 Password: ")
    else:
        print("pass=" + sys.stdin.read().strip())
    return sys.stdin.read().strip()

parser = OptionParser()
parser.add_option("--delete", dest="delete", action="store_true", help="Delete all E-mails when attachment was saved")
parser.add_option("--hostname", dest="hostname", help="Hostname POP3 Mailserver")
parser.add_option("--username", dest="username", help="POP3 Username")
parser.add_option("--password", dest="password", help="POP3 Password")
parser.add_option("--downloadpath", dest="downloadpath", help="Download Path")

(options, args) = parser.parse_args()

if not options.hostname:
    parser.error('--hostname parameter required')
if not options.username:
    parser.error('--username parameter required')
if not options.downloadpath:
    parser.error('--downloadpath parameter required')

if options.password is None:
    options.password = getpass(prompt='POP3 password ')
     
class InfoFilter(logging.Filter):
    def filter(self, rec):
        return rec.levelno in (logging.DEBUG, logging.INFO)

std_out_stream_handler = logging.StreamHandler(sys.stdout)
std_out_stream_handler.setLevel(logging.DEBUG)
std_out_stream_handler.addFilter(InfoFilter())
std_out_stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

std_err_stream_handler = logging.StreamHandler(sys.stderr)
std_err_stream_handler.setLevel(logging.WARNING)
std_err_stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(std_out_stream_handler)
root_logger.addHandler(std_err_stream_handler)


t = time.localtime() * 1000
timestamp = time.strftime("%d%m%y_%H%M")


def save_attachment(mstring):

    filenames = []
    attachedcontents = []

    msg = Parser().parsestr(mstring)

    for part in msg.walk():

        fn = part.get_filename()

        if fn != None:
            filenames.append(fn)
            attachedcontents.append(part.get_payload(decode=True))

    for i in range(len(filenames)):
        download_filename = timestamp + time.strftime("%S") + "_" + filenames[i]
        download_path = os.path.join(options.downloadpath, download_filename)
        os.makedirs(os.path.dirname(os.path.abspath(options.downloadpath)), exist_ok=True)

        time.sleep(2)
        with open(download_path, "wb") as fp:
            fp.write(attachedcontents[i])
            logging.info('Attachment from message was saved to %s', download_path)
        fp.close()


try:
    logging.info('Login in to %s as %s', options.hostname, options.username)
    connection = poplib.POP3_SSL(options.hostname)
    connection.user(options.username)
    connection.pass_(options.password)
    logging.info('Message from %s: %s', options.hostname, connection.getwelcome().decode())
except:
    logging.exception('Login to %s was not possible', options.hostname)
    sys.exit(1)
logging.info('Login to %s as %s was successful', options.hostname, options.username)

anzahl_mails = len(connection.list()[1])
count_mails = int(anzahl_mails)

if count_mails == 0:
    logging.info('Inbox is empty. Logout from server')
    connection.quit()
    sys.exit(1)
else:
    logging.info('Inbox has %s unread E-mails. Try to proceed them', count_mails)
    for i in range(count_mails):  
        counter = i + 1
        lines = connection.retr(counter)[1]
        mailstring = b"\r\n".join(lines).decode("utf-8")
        save_attachment(mailstring)
        if options.delete:
            connection.dele(counter)
            logging.info('All E-mails were deleted')
connection.quit()
logging.info('All attachments were downloaded. Logout from server')
time.sleep(2)
sys.exit(1)