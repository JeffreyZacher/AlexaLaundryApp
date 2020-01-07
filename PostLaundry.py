import requests
import re
import urllib.parse

# Url of the website to get the information from
url = "https://www.mywavevision.com/Index.aspx"

# Creates the body of the call
# needs to have a file called Credentials.txt in the same directory as this file and with line1 being username and line2 being password
# Username must have no spaces in it
def GetPayload(viewState):
    viewStateEncoded = urllib.parse.quote(viewState, safe='')

    credentials = open("Credentials.txt", "r").read().splitlines()
    return "__VIEWSTATE={}&__VIEWSTATEGENERATOR={}&txtUserID={}&txtPassword={}&btnLogin=Login".format(viewStateEncoded, "203A92CB", credentials[0], credentials[1])

# Creates the Headers of the call Session_ID is set to expire in 29 years so it doens't need updated
def GetHeaders():
    return {
    'Connection': "keep-alive",
    'Cache-Control': "max-age=0",
    'Upgrade-Insecure-Requests': "1",
    'Content-Type': "application/x-www-form-urlencoded",
    'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    'Accept-Encoding': "gzip, deflate, br",
    'Accept-Language': "en-US,en;q=0.9",
    'Cookie': ",ASP.NET_SessionId=maiylawoaknajvib5yy00vct; LoginUserName=",
    'Postman-Token': "5b272aa1-9096-45c7-bf63-6b221898ef4c,5ff60f3c-4629-44a0-95e3-5553542c26a1",
    'cache-control': "no-cache"
    }

def GetMachines():
    # this request is just so we can grab the Viewstate from the response since that will change over time
    response = requests.request("POST", url, data=GetPayload(""), headers=GetHeaders())

    # This request will return the new page that contains machine data
    if "<title>Welcome to WaveVision</title>" in response.text:
        response = requests.request("Post", url, data=GetPayload(re.findall(r"id=\"__VIEWSTATE\" value=\"(.*)\" /\>", response.text)[0]), headers=GetHeaders())

    # this will create a tuple of the machines and their availability
    return re.findall(r"ContentPlaceHolder1_gvRoom_lblMachineID_\d\"\>(\w+\s\d)(?:.*\n){5}.*ContentPlaceHolder1_gvRoom_lblStatus_\d\"\>(\w+)", response.text)