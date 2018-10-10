"""
zmail.api
~~~~~~~~~~~~
This module implements the zmail API.
"""
import logging
from typing import Optional

from .info import get_supported_server_info
from .message import mail_decode
from .server import MailServer
from .utils import get_attachment, get_html, read, save, show

logger = logging.getLogger('zmail')

# Backward-compatible with earlier versions.
read_eml = read
save_eml = save

__all__ = ['get_attachment', 'get_html', 'show', 'read', 'save', 'server', 'decode', 'read_eml', 'save_eml']


def server(username: str, password: str,
           smtp_host: Optional[str] = None,
           smtp_port: Optional[int] = None,
           smtp_ssl: Optional[bool] = None,
           smtp_tls: Optional[bool] = None,
           pop_host: Optional[str] = None,
           pop_port: Optional[int] = None,
           pop_ssl: Optional[bool] = None,
           pop_tls: Optional[bool] = None,
           config: Optional[str] = None,
           timeout=60, debug=False, auto_add_to=True, auto_add_from=True):
    """A wrapper to MailServer.

    SMTP:
        server.send_mail([recipient,], mail)

    POP3:
        server.get_mail(which)
        server.get_mails(subject, sender, after, before)
        server.get_latest()
        server.get_info()
        server.stat()

    Parse mail:
        server.show(mail)
        server.get_attachment(mail)
    """

    user_define_config = {
        'smtp_host': smtp_host,
        'smtp_port': smtp_port,
        'smtp_ssl': smtp_ssl,
        'smtp_tls': smtp_tls,
        'pop_host': pop_host,
        'pop_port': pop_port,
        'pop_ssl': pop_ssl,
        'pop_tls': pop_tls,
    }

    auto_generate_config = get_supported_server_info(username, config)  # type:dict

    auto_generate_config.update({k: v for k, v in user_define_config.items() if v is not None})

    # Ignore IMAP config.
    auto_generate_config = {k: v for k, v in auto_generate_config.items() if 'imap' not in k}

    return MailServer(username, password, **auto_generate_config, timeout=timeout, debug=debug,
                      auto_add_to=auto_add_to, auto_add_from=auto_add_from)


def decode(mail_as_bytes, which=1):
    """Decode bytes mail, as usual in your disk."""
    return mail_decode(mail_as_bytes, which)
