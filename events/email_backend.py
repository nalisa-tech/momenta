"""
Custom Email Backend for Nalisa Events
=====================================

This custom backend fixes compatibility issues with Gmail SMTP.
"""

import smtplib
import socket
from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings


class GmailEmailBackend(EmailBackend):
    """
    Custom Gmail SMTP backend that fixes starttls() issues
    """
    
    def __init__(self, host=None, port=None, username=None, password=None,
                 use_tls=None, fail_silently=False, use_ssl=None, timeout=None,
                 ssl_keyfile=None, ssl_certfile=None, **kwargs):
        super().__init__(host, port, username, password, use_tls, fail_silently, 
                        use_ssl, timeout, ssl_keyfile, ssl_certfile, **kwargs)
        
        # Set local_hostname if not already set
        if not hasattr(self, 'local_hostname') or self.local_hostname is None:
            self.local_hostname = socket.getfqdn()
    
    def open(self):
        """
        Ensure we have a connection to the email server. Return whether or not a
        new connection was required (True or False).
        """
        if self.connection:
            # Nothing to do if the connection is already open.
            return False

        # Connection parameters
        connection_params = {}
        if self.local_hostname:
            connection_params['local_hostname'] = self.local_hostname
        if self.timeout is not None:
            connection_params['timeout'] = self.timeout
            
        try:
            self.connection = smtplib.SMTP(self.host, self.port, **connection_params)

            # TLS/SSL are mutually exclusive, so only attempt TLS over
            # non-secure connections.
            if not self.use_ssl and self.use_tls:
                # Use simple starttls() without keyfile/certfile parameters
                self.connection.starttls()
                
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except (smtplib.SMTPException, OSError):
            if not self.fail_silently:
                raise