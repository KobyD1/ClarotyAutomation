import pandas as pd
import json
import smtplib
from email.message import EmailMessage

from globals import JSON_PATH, EMAIL_ADDRESS, EMAIL_PASSWORD


class MailUtils():

    def __init__(self, logger):
        self.logger = logger
        self.msg = EmailMessage()

    def get_max_price(self, path=JSON_PATH):
        self.logger.info(f"Trying to get Max price from saved JSON")

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        df = pd.DataFrame(data)
        df['price'] = pd.to_numeric(df['price'])

        max_price = df['price'].max()
        self.logger.info(f"Max Price found the value is : {max_price}")
        return max_price

    def send_gmail(self, mail_as_dict):
        self.logger.info("Trying to send mail")

        self.msg['Subject'] = mail_as_dict['subject']
        self.msg['From'] = EMAIL_ADDRESS
        self.msg['To'] = mail_as_dict['to']
        self.msg.set_content(mail_as_dict['content'])
        self.logger.debug(f" mail details : {mail_as_dict}")

        with open(mail_as_dict["attachment"], 'rb') as f:
            file_data = f.read()
            file_name = f.name

        self.msg.add_attachment(
            file_data,
            maintype='image',
            subtype='png',
            filename=file_name
        )
        self.msg.add_attachment(mail_as_dict['attachment'])

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                smtp.send_message(self.msg)
            self.logger.info("Send mail success")

        except Exception as e:
            print({e})
            self.logger.info("Send mail failed")
