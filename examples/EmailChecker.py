import time
import imaplib
import pprint


imap_ssl_host = 'imap.cern.ch'  # imap.mail.yahoo.com
imap_ssl_port = 993
server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
server.login('jruizalv', 'Tumbo-Tambo-1315')
server.select('INBOX/EXO MC Contact/McM announcement/To me')

#tmp, data = server.search(None, 'SUBJECT', '[McM] Status changed for request to new', 'BODY', 'EXO-RunIIFall18pLHE-00127')
tmp, data = server.search(None, 'SUBJECT', 'run test failed for request', 'BODY', 'EXO-RunIIFall18GS-02185')

for num in data[0].split():
	tmp, MessageContent = server.fetch(num, '(RFC822)')
	print('Message: {0}\n'.format(num))
	pprint.pprint(MessageContent[0][1])
	break

server.logout()
