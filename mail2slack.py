#!/usr/bin/env python
""" Connect to an mailbox via IMAP, read e-mail messages and send them through Slack """

import os
import sys
import imaplib
import logging
import configparser
import argparse
import time
from datetime import datetime
import mailparser
from slack import WebClient
from slack.errors import SlackApiError
from version import __version__


# Initialize LOGGER function
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
LOGGER = logging.getLogger()
#LOGGER.setLevel(logging.INFO)

def get_text(message):
    """ Get content of email and return a string """

    for part in message.walk():  # in depth-first traversal order 1
        if part.get_content_maintype() == 'text':

            text = part.get_payload(decode=True)
            return part.get_content_type(), text
        if part.get_content_type() == 'multipart/alternative':
            # in an order of increasing faithfulness 3
            for altpart in reversed(part.get_payload()):
                text = get_text(altpart)
                if text is not None:
                    return text
        continue
    return None


def process_mailbox(config, mailbox):
    """ Main flow to process mailbox folder selected previously """
    
    client = WebClient(token=config['token'])
    api_response = client.api_test()        

    receive, data = mailbox.search(None, "UNSEEN")
    if receive != 'OK':
        LOGGER.info('No messages found!')
        return        

    for num in data[0].split():

        typ, data = mailbox.fetch(num, '(RFC822)')
        if typ != 'OK':
            LOGGER.error("ERROR getting %d message", num)
            return

        mail = mailparser.parse_from_bytes(data[0][1])

        plain =  ' '.join(mail.text_plain)
        plain = plain.replace('"', '\\"')
        plain = plain.replace('<', '&lt;')
        plain = plain.replace('>', '&gt;')
        plain = plain.replace('&', '&amp;')
        plain = plain.replace('\r', ' ') 

        LOGGER.debug("mail.subject: %s", mail.subject)
        print(f"send: {mail.subject} ")

        try:
            response = client.chat_postMessage(channel=config['channel'],                 
            blocks=[
                        {
                            "type": "divider"
                        },
                        {
                            "type": "header",
                            "text": {
                                "type": "plain_text",
                                "text": ":newspaper: " + mail.subject ,
                            }
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "text": " *" + mail.from_[0][1] + "*" ,
                                    "type": "mrkdwn"
                                }
                            ]
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": plain, 
                            }
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "context",
                            "elements": [
                                {
                                    "type": "mrkdwn",
                                    "text": config['title_link']
                                }                        
                            ]
                        }
                    ]    
            )
        except SlackApiError as e:        
            if response.status_code != 200:
                LOGGER.error('Request to slack returned an error %s, the response is: %s - content: %s',
                            response.status_code,
                            response.text
                            #payload
                            )    
            else:
                # other errors
                raise e                                     

        # Not too fast...
        time.sleep(5)


def process_mails():
    """ Main flow to process mailbox messages """
    parser = argparse.ArgumentParser(
        description="Script to read new e-mails from mailbox via IMAP parse content and send to Slack endpoint")

    parser.add_argument("-d", "--debug", action='store_true')
    parser.add_argument("-c", "--config", default=os.path.dirname(os.path.abspath(__file__)) + '/mail2slack.conf')
    args = parser.parse_args()

    if args.debug:
        LOGGER.setLevel(logging.DEBUG)
        LOGGER.debug("DEBUG Mode is ON")

    LOGGER.debug("Config file path: %s", args.config)

    config = {}
    config_f = configparser.ConfigParser()

    try:
        read_config_file(config_f, args, config)
    except configparser.ParsingError:  # Corrected from configparser.ConfigParser.ParsingError
        LOGGER.error("Unable to parse config from file %s!", args.config)
        sys.exit(1)

    mailbox = imaplib.IMAP4_SSL(config['mailserver'])

    try:
        mailbox.login(config['mail_login'], config['mail_pw'])
    except imaplib.IMAP4.error:
        LOGGER.error("IMAP LOGIN FAILED!!!")
        sys.exit(1)

    receive = mailbox.select(config['folder'])
    if receive[0] == 'OK':
        process_mailbox(config, mailbox)
        mailbox.close()
    else:
        LOGGER.error("Unable to read from mailbox %s!", config['folder'])

    mailbox.logout()


def read_config_file(config_f, args, config):
    config_path = args.config
    missing_config = False  # Flag to indicate missing configuration
    if os.path.exists(config_path):
        with open(config_path) as config_file:
            config_f.read_file(config_file)
        for section in config_f.sections():
            for option in config_f.options(section):
                env_var_name = f"{section}_{option}".upper()
                config[option] = config_f.get(section, option, fallback=os.getenv(env_var_name))
    else:
        schema = {
            'SLACK': ['end_point', 'slack_sender', 'icon_url', 'slack_fallback', 'channel', 'token'],
            'MAIL': ['mailserver', 'mail_login', 'mail_pw', 'folder', 'author_link', 'title_link', 'footer', 'footer_icon'],
            'GENERAL': ['log_level']
        }
        for section, options in schema.items():
            for option in options:
                env_var_name = f"{section}_{option}".upper()
                env_var_value = os.getenv(env_var_name)
                if env_var_value is None:
                    LOGGER.error(f"Missing required configuration: {env_var_name}")
                    missing_config = True
                else:
                    config[option] = env_var_value

    # Check for 'LOG_LEVEL' environment variable or 'log_level' in config dictionary with a default of 'INFO'
    log_level_name = os.getenv('LOG_LEVEL') or config.get('log_level', 'INFO').upper()
    # Convert log level name to a logging level and apply it
    log_level = logging.getLevelName(log_level_name)
    LOGGER.setLevel(log_level)

    if missing_config:
        LOGGER.error("Application configuration is incomplete. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    LOGGER.info(f"...Starting mail2slack version: {__version__}...")
    while True:
        LOGGER.debug(f"Starting process_mails: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        process_mails()        
        time.sleep(10)




