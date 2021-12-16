## PyPopAttachDown.py Python POP3 E-mail attachment downloader
=====================

Simplified tool for downloading attachments of POP3 E-mails and delete the processed E-mails

# Usage:

Usage: attachment-downloader [options]

Options:
-h, --help            show this help message and exit
--hostname=HOST       Mailserver Hostname
--username=USERNAME   POP3 Username
--password=PASSWORD   POP3 Password
--downloadpath=DOWNLOADPATH
Folder in which the attachments are downloaded
Please consider difference between UNIX based (/path/to/download)
and Windows based paths (D:\\Path\\To\\Download)
--delete       
Delete downloaded emails from Mailbox



# Example:

$ PyAttachDown.py --hostname=pop.kabelmail.de --username=foo.bar@foo.com --downloadpath=/tmp/attachents --password=FooBar --delete



Heavily inspired from the great work of abgdf@gmx.net and noPlan (attsave.py script) and the IMAP attachment downloader https://github.com/jamesridgway/attachment-downloader