#!/usr/bin/python

import requests

url = "https://wsbs.jiangxi.chinatax.gov.cn/syhdfw/ws/apiRequestServer"


headers = {
    'Content-Type': 'text/xml; charset=utf-8',
    'Accept': 'application/soap+xml, application/dime, multipart/related, text/*',
    'User-Agent': 'Axis/1.4',
    'Cache-Control': 'no-cache',
    'Pragma': 'no-cache',
    'Soapaction': "invoke"
}

request_data = '<?xml version="1.0" encoding="UTF-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><ns1:invoke soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:ns1="http://ws.api.aisino.com/"><requestXml xsi:type="xsd:string">QjlEMDhFNzhENURBMEUzNkI2RUIzRTc5NjEwMUExMzMzQjQ1QzU2MEIzOTM0OEQxM0MyQTJGM0NEQkExODQ1REZBQTE4RjNGREEwOTlGQzE0QTJGOTJFRDU1RTlBQ0U2RThFOENEQ0NFRDVDOTJERUUyOTMyNjlFMUY2NUJCNDVFQkY4OEE1NzNBRUY5N0Q4NDkwMTRBOEZBMUVEOTg3RUY0NzczODFBMDYzQkZGRTEyRDE1Qjk0NUQ0MDAzMzVGQjZBRjRFRjQwNDFBM0NDMzdGRDZFOUU3QzU5OEM4MEI2MEE2M0FDOTkzOUY0RjZCQjUyMEY0ODY0RjM1ODY5NTUwMUJDNzFCRDU5ODg0QTFFMzBGQTIzNkQzOTQ3Qzc3MDIxMEVBODRDODVCNjBGM0QxODAwRDZBQThEQkIxRDEyQjFDNERBQkY4NDk2RjA3NEQ4MTM5NzYyQzcwMzU1QTUxNjUzOTJERUYwMzkzRTM3ODM0NkYwNjc0RTFGQTU3MTEyMUJEREQ2NTk4M0QwNkY2OTBBNjMzMDVGNzQ0OTZGNDEwNThCNjdBQjFCOEQ5REE5MUU1RkZFMUY4QTI3Q0M5ODI2OTI1MUUyNzMzNDNGMjQ4MDU3N0ExRDMzQTVEMTU3MEQyRThCNzdDMThGMTFFQkMzQzYwNTk4RDk2NzhBODVBREM4RTQyMUI1RTQ3NjI0QTlBRjk4Q0ZGNUE4QUJGRTU0NDkzOTMyM0IzRTMwOTFGMzQwMURGODVDNURGMDBERjdBREQxMjRFQTc1OTBCODdBQkYwNDM0RkIwNEY5OUFCN0VCMTg4RjdGMkM3RUYxNTVFNzRFRkVFODIzNzU5OEQ5Njg1MkI2OTAwMkRENUYyOUE4NjA0MUQ4NjE2RkQxMkI1QzREMTQ2OTQyMDBERTJDQ0I3MjE3MDhDRTY2QkE1QTRCNjkwNDI2RUJGRTNDNzI3RkMwODZEMDg2OTRCQzYwMzdFOTRDMjBENjYzNzExNTA3MTJERDRCMTQ4NDQ3QTlCRkIwQTgwMEVERDg1NzAwQzMyMDA2NEQwMEMwNDI5MkFDNjU0NzFDNTY1QkExMjIwMjFCMUZGMzhCRUYyQzA4MTY5ODZDRjQxRTJDM0FDQjhDQkM0NURGQjYxREVFRkYzMjE2NEUyNkQzRkYxRUQyNDA1QzVGOEMwNjYwM0RBODE1RDA3MDM5RjAxOTk3MDQ0RjRFREFEMDk2QkI0REUwRjEwRUU0OEFGNzg2MEFFNTA0RDQ1MTE4QzU3</requestXml></ns1:invoke></soapenv:Body></soapenv:Envelope>';

response = requests.post(url, data=request_data, headers=headers)

print(response.content)