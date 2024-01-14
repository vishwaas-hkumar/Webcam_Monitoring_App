import smtplib
import imghdr
#import filetype
#metadata of images for subtype, maintype
from email.message import EmailMessage

PASSWORD = "hijgydugfxlqwfib"
SENDER = "vishkumar0502@gmail.com"
RECEIVER = "vishkumar0502@gmail.com"
def send_email(image_path):
    print("send_email fn started")
    #print("Email Sent")
    email_message = EmailMessage()
    email_message ["Subject"] = "Incoming!!!"
    email_message.set_content("Someone just showed up.")

    with open(image_path,"rb") as file:
        content = file.read()
    email_message.add_attachment(content, maintype="image",subtype=imghdr.what(None,content))

    #sending email
    gmail = smtplib.SMTP("smtp.gmail.com", 587) #port for GMail
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER,RECEIVER, email_message.as_string())
    gmail.quit()
    print("send_email fn ended")
if __name__ == "__main__":
    send_email(image_path="images/20.png")
