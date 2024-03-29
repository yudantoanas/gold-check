from bs4 import BeautifulSoup
from selenium import webdriver
import chromedriver_autoinstaller
import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Since in the GH action we use xfvb for virtual display,
# so we need to implement this package in order to work
from pyvirtualdisplay import Display

def sendMail(message: dict):
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login("youdant@gmail.com", "mhij klyz msau mslr")

    # message to be sent
    sender_email = "youdant@gmail.com"
    receiver_email = "yudanto.testbench@gmail.com"
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Harga Emas {'Naik' if message['isUp'] else 'Turun'}!"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    html = f"""\
    <html>
    <body>
        <p>Hi,<br>
        Harga Emas Hari ini sedang {'Naik' if message['isUp'] else 'Turun'}</p>
        <p>Rp {message['price']}</p>
        <p>{'Kenaikan' if message['isUp'] else 'Penurunan'} sebesar Rp {message['diffPrice']}</p>
    </body>
    </html>
    """
    part = MIMEText(html, "html")
    msg.attach(part)

    # sending the mail
    s.sendmail(sender_email, receiver_email, msg.as_string())

    # terminating the session
    s.quit()

    print("email sent!")


def startScrape():
    chromedriver_autoinstaller.install()

    driver = webdriver.Chrome()

    url = "https://www.brankaslm.com/antam/index"
    driver.get(url)
    html = driver.page_source

    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")

    # get price
    td = table.find("td", {"class": "text-right"})
    fullString = td.getText().split('\n')
    price = fullString[1].strip()
    diffPrice = fullString[2].strip()

    # check up/down
    arrow = td.find("i", {"class": "fa fa-caret-up"})

    result = {
        'price': price,
        'diffPrice': diffPrice,
        'isUp': arrow != None,
    }

    driver.quit()

    return result


if __name__ == "__main__":
    display = Display(visible=0, size=(800, 800))
    display.start()
    res = startScrape()
    sendMail(res)
