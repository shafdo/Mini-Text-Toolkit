#!/usr/bin/python3

from urllib.parse import quote, quote_from_bytes
import os, shutil, base64, codecs, html, binascii, sqlite3, tempfile, webbrowser
from bs4 import BeautifulSoup
from datetime import datetime
try: 
    import PySimpleGUI as sg 
except(ModuleNotFoundError):
    print("[-] Module not found: pysimplegui\n[-] Try pip install pysimplegui")
    exit()


# Globals
currentDir = os.path.dirname(__file__)
sgThemeGlobal = ""
platform = "windows" if(os.name) else "linux"

# Icons
aboutImgData = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAsTAAALEwEAmpwYAAAFP0lEQVR4nO2Y7U9TVxzHGXvp9hcse7f1uaVPSQtuMxmSZWuoXUYMwqI4tbzwxabR1czE4KagYWlLl2I7kLbJeNgLN6ZbdFBELSAlS5SRLBKzFyzbMhITH0qviobffqeu19729nIv9CHc3W/yDYHb8zu/7+dezj09FRWSJEmSJEmSJEmSiiOz2bzFZDL1G43GOfTvPD1HxhgMhrfK3f+6hEFOYxBYj0mNcudYk7D5vesNn+E95c4jVC9g0wssd/MH/HkE7crjI/iZYRYAC6RmuUPxFv7vvsYSPsJ3PH4+nD2e1CxmzwUVNmxhuYsNAsY3sACoLmbPBRXebWt2AHwb2PmOx7D1LONritlzQSUKAAAVlY8m7bbkhL19KeZwC/Gt720DoRO1kOkb39qG+Y6/MfTucPb4376zDQntI9X7VbtNcPjERP2HVLw58fCXfSAGU9PNicSUvZlXeGpqWxM189FKuZsuOATMlLj23o7VAVxvus8YPNOC3rVB3ZL9JNzjDP94qn77s9C7gbr2DiRHTbA0atjQTkbNqSwkUwpCrH47x+P/wRihlrxcXfbGCw4CM5Fs1FRDND8AXPiSV98ue7NFg3ClNrUgsoZ/MG1XUTM7y95ksU0yJsZtmhwAySlHX3JyW9kbLPpTgBmpSUdvDoCH041/Jq9sKXuDRQeAGSnMyggPP9dtouK7VpZGjbwL3R8xw4+Rw9B/9jRMDu4ueZDY4B74pvcUXIgcggdC3lZRE1DxlhWYsL9MAzi23+I62lp958BO7Xw+H26pmh84rr6TdtDtWg6Hw5ByKAR97fZE+lrvUc0iV621uPczzWK6fl+7I0HPjf7a/elyZm+HWrS3uWqRrMf2V7toAHK5/JRMJgMuW0wyuPjl67R7zrghs4mw72P62qhHzllrLR7Bmun64a5PGHP3BNyM3qym1efHzB00AK1Wu1U4AA+jiZDvQOkA+A4y5u4NeAUDwMy1mcvAi2q1+qlOp4N83mzVwe0hDe2g73Po7u6mPfiVk742EdDkrbNWx848n3vQ38qYm/SS2dtmC3ctlUr1lGRmLIRI5G+ug8k3apgLpL/DCW1tbbTP+x30tZk+Q6EOQ2nHzz6f+7z/fcbc/o5WRm9v1nDXwqx/5bwG8Y+z6wFwobuUABzrBXAzB4BGo4kKARDqbGI0Md6ztWQALvfUMeYOde4QCmCEDcCQEACxgB48Xzih/bgLgu2NMD+gKRmAW/1qCJxshJM4t/eEE9cHvSAAmHUgBwAugl1CANwMqxgr7x/ndCUDsHBOy5h7NqLiDcBoNAJmdecAwJXRSS7yBXD3oh6mg0oY88rg14iaca3YAIhn8QaQueNBBdy9xP8JMBgMBMDeHABVVVV6NG8AXC4FAC5zAdDr9cRVOQBQlfiOXBY7AMz4mGRlA8C5FxALANY9QAaAvHsBEQHI3QOkxbUXEBGA3D1ABoBBsQMgGbkAeMUMgLzmMaMnLwDcC+zLtxcQCwDWPUBaXHsBMQAg2fLtAdKqxEWCdS8gBgCce4CMdWBRrADw5v7DGf6/dYB1MyQGACQbHwBzaNEBIJmUSuUcHwBecmiIH059cUi/FTYiANI7yUCykEysX4NZALykUCgeZRwfA/4OVrMCxn1yXh7rUqTGFNLRLiXv+avNytQY0ns6B8mEi+CmVQEQ4UJYh4OecB2Lc7nYx+KrOftYHEE8IUf/vMKnhY/Lq/g0jCC5e1hg2WKQL0c9MuDjnzoVK2RMIU1q8p3fan42hvSOGS7h+/8VQeElSZIkSZIkSZL+D/oXjKMfxw94DhgAAAAASUVORK5CYII='
warningImgData = b'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'
tickImgData = b'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'
errorImgData = b'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'

class historyLogger():
    def createDB(self):
        conn = sqlite3.connect('.mtt-history.db')
        # if(platform == "windows"): os.system("attrib +h .mtt-history.db")
        cursor = conn.cursor()
        try:
            cursor.execute('CREATE TABLE history ( id INTEGER PRIMARY KEY AUTOINCREMENT, today DATE, time INTEGER, convertFrom TEXT, convertValue TEXT )')
        except(sqlite3.OperationalError):
            pass
        return conn

    def resetDB(self, conn):
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM history;")
            conn.commit()
            return True

        except(sqlite3.OperationalError):
            return False


    def log(self, conn, convertFrom, convertValue):
        cursor = conn.cursor()
        today = datetime.today().strftime("%b-%d-%Y")
        time = datetime.today().strftime("%H:%M")
        query = "INSERT INTO history(today, time, convertfrom, convertvalue) VALUES (?,?,?,?)"
        cursor.execute(query, (today, time, convertFrom, convertValue))
        conn.commit()
        

    def display(self, conn):
        ''' History Output Structure
        /\/\/\/\/\/\/ DATE /\/\/\/\/\/\/
        ConvertFromType     Value
        Ex: Binary          1001110
        '''
        cursor = conn.cursor()
        content = {}

        for row in cursor.execute("SELECT DISTINCT today FROM history ORDER BY today DESC;"):
            content[str(row[0])] = []

        for key, value in content.items():
            query = "SELECT id, time, convertFrom, convertValue FROM history WHERE today='{}'".format(key)
            for row in cursor.execute(query):
                content[key].append(row)

        return content

    
    def createTempFolder(self):
        return tempfile.mkdtemp()


    def removeTempFolder(self, tempFolderPath):
        shutil.rmtree(tempFolderPath)


    def webTempFile(self, tempFolderPath, html):
        tempFile = os.path.join(tempFolderPath, "{}.html".format(next(tempfile._get_candidate_names())))
        print(tempFile)

        # Write default HTML stuff
        defaultDocumentHTML = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta name="viewport" content="width=device-width,initial-scale=1"><title>MTT History</title></head><body><style>body{background-color:#222}.row{margin-bottom:50px}.para-wrapper{margin-left:25px;padding-left:15px;border-left:4px solid #ff007b}.divider{border:none;border-bottom:4px solid #ff007b}.green{color:#53e623}h2{color:#37b2ca}.text-white{color: #c1c1c1}p{font-size:18px;color:#c1c1c1;font-family:Ubuntu,sans-serif;line-height:30px}.pl-4{padding-left:10px}#content{margin:25px}#heading{color:#ffe000;font-family:Ubuntu,sans-serif;}</style><h1 id="heading">MTT Histroy</h1><ul class="text-white"><li><p class="pl-4">Thank you for trying out MTT :).</p></li></ul><div id="content"></div></body></html>'
        soup = BeautifulSoup(defaultDocumentHTML, "html.parser")
        soup.find("div", {"id": "content"}).append(BeautifulSoup(html, 'html.parser'))

        f = open(tempFile, "w")
        f.write(soup.prettify())
        f.close()

        webbrowser.open(tempFile)


conn = historyLogger().createDB()
tempFolderPath = historyLogger().createTempFolder()
print(tempFolderPath)


class Convertor():

    def paddingFixer(self, convertValue, skipper):
        allXChars = [i for i in convertValue]
        bitsSplitContainer = []

        while 1:
            if(len(allXChars) == 0): break

            elif(len(allXChars) >= skipper):
                bitsSplitContainer.append("".join(allXChars[:skipper]))
                del allXChars[:skipper]

            else: allXChars.insert(0, "0")

        return "".join(bitsSplitContainer)

        # stringLine to list => [result[i:i+skipper] for i in range(0, len(result), skipper)]


    def fromAscii(self, convertMethod, convertValue):
        if(convertMethod == "ascii2bin"):
            allChars = [i for i in convertValue]
            binariesContainer = []
            for char in allChars:
                binaryVal = bin(ord(char)).replace("0b", "0")
                if(len(binaryVal) == 8): binariesContainer.append(binaryVal)
                else:
                    binariesContainer.append("0" * (8 - len(binaryVal)) + binaryVal)

            return " ".join(binariesContainer)

            # Old Method (Works but prone to some error).
            # return "0" +' 0'.join(format(ord(x), 'b') for x in convertValue)
       
        if(convertMethod == "ascii2hex"):
            return " ".join("{:02x}".format(ord(x)) for x in convertValue)

        if(convertMethod == "ascii2base64"):
            return base64.b64encode(convertValue.encode()).decode("utf-8")

        if(convertMethod == "ascii2dec"):
            return " ".join([str(ord(x)) for x in convertValue])

        if(convertMethod == "ascii2rot13"):
            return codecs.encode(convertValue, "rot_13")

        if(convertMethod == "ascii2rot47"):
            # Found this method of representing ROT47 from https://rot47.net/
            x = []
            for i in range(len(convertValue)):
                j = ord(convertValue[i])
                if j >= 33 and j <= 126:
                    x.append(chr(33 + ((j + 14) % 94)))
                else:
                    x.append(convertValue[i])
            return ''.join(x)

        if(convertMethod == "ascii2urlencode"):
            return quote(convertValue, 'utf-8')

        if(convertMethod == "ascii2htmlentities"):
            return html.escape(convertValue)
        

    def fromBin(self, convertMethod, convertValue):
        if(convertMethod == "bin2ascii"):
            try:
                return binascii.unhexlify('%x' % int(str(convertValue), 2)).decode("ascii", "ignore")
            except(UnicodeDecodeError):
                return "�"

            except ValueError:
                return ""

        if(convertMethod == "bin2hex"):
            if(len(convertValue) % 8 == 0):
                hexValWithout0x = hex(int(convertValue, 2))[2:]
                hexValSpaceInBetween = " ".join([hexValWithout0x[i:i+2] for i in range(0, len(hexValWithout0x), 2)])
                return hexValSpaceInBetween
            
            else:
                # Fix Padding
                return self.fromBin("bin2hex", self.paddingFixer(convertValue, 8))

        if(convertMethod == "bin2base64"):
            getAscii = self.fromBin("bin2ascii", convertValue)
            return base64.b64encode(getAscii.encode()).decode("utf-8")

        if(convertMethod == "bin2decimal"):
            decimalNumContainer = []
            if(len(convertValue) % 8 == 0):
                valuesSplitBy8 = [convertValue[i:i+8] for i in range(0, len(convertValue), 8)]
                for val in valuesSplitBy8: decimalNumContainer.append(int(val, 2))
                temp = [str(val) for val in decimalNumContainer]
                return " ".join(temp)

            else:
                # Fix Padding
                return self.fromBin("bin2decimal", "".join(self.paddingFixer(convertValue, 8)))

        if(convertMethod == "bin2rot13"):
            asciiVal = self.fromBin("bin2ascii", convertValue)
            rot13Val = self.fromAscii("ascii2rot13", asciiVal)
            return rot13Val

        if(convertMethod == "bin2rot47"):
            asciiVal = self.fromBin("bin2ascii", convertValue)
            rot47Val = self.fromAscii("ascii2rot47", asciiVal)
            return rot47Val

        if(convertMethod == "bin2urlencode"):
            asciiVal = self.fromBin("bin2ascii", convertValue)
            urlEncoded = self.fromAscii("ascii2urlencode", asciiVal)
            return urlEncoded
        
        if(convertMethod == "bin2htmlentities"):
            asciiVal = self.fromBin("bin2ascii", convertValue)
            htmlEncoded = self.fromAscii("ascii2htmlentities", asciiVal)
            return htmlEncoded
       

    def fromHex(self, convertMethod, convertValue):
        if(convertMethod == "hex2ascii"):
            try:
                bytes_object = bytes.fromhex(convertValue.replace("0x", ""))
                asciiString = bytes_object.decode("ASCII")
                return asciiString
            except:
                return ""

        if(convertMethod == "hex2bin"):
            binaryString = bin(int(convertValue, 16))[2:].zfill(8)
            return " ".join([binaryString[i:i+8] for i in range(0, len(binaryString), 8)])

        if(convertMethod == "hex2base64"):
            asciiString = self.fromHex("hex2ascii", convertValue)
            return base64.b64encode(asciiString.encode()).decode("ASCII")

        if(convertMethod == "hex2decimal"):
            if(len(convertValue) % 2 == 0):
                hexPairContainer = []
                for hexPair in [convertValue[i:i+2] for i in range(0, len(convertValue), 2)]: hexPairContainer.append(str(int(hexPair, 16)))
            
                return " ".join(hexPairContainer)

            else:
                # Fix Padding
                return self.fromHex("hex2decimal", self.paddingFixer(convertValue, 2))

        if(convertMethod == "hex2rot13"):
            asciiVal = self.fromHex("hex2ascii", convertValue)
            rot13Val = self.fromAscii("ascii2rot13", asciiVal)
            return rot13Val

        if(convertMethod == "hex2rot47"):
            asciiVal = self.fromHex("hex2ascii", convertValue)
            rot47Val = self.fromAscii("ascii2rot47", asciiVal)
            return rot47Val
        
        if(convertMethod == "hex2urlencode"):
            asciiVal = self.fromHex("hex2ascii", convertValue)
            urlEncoded = self.fromAscii("ascii2urlencode", asciiVal)
            return urlEncoded
        
        if(convertMethod == "hex2htmlentities"):
            asciiVal = self.fromHex("hex2ascii", convertValue)
            htmlEncoded = self.fromAscii("ascii2htmlentities", asciiVal)
            return htmlEncoded


    def fromBase64(self, convertMethod, convertValue):
        if(convertMethod == "base642ascii"):
            try:
                return "".join([chr(i) for i in base64.standard_b64decode(convertValue)])
                
                # Previous solution: Strips up unicode characters too
                # return base64.b64decode(convertValue).decode("ascii", "ignore")
            
            except(UnicodeDecodeError):
                return "�"

            except ValueError:
                return ""

        if(convertMethod == "base642bin"):
            # To decode base64 format you need to pass a bytes object to the base64.decodebytes(). Reference: https://stackoverflow.com/a/43208125 
            base64Decoded = base64.decodebytes(convertValue.encode())
            return " ".join(["{:08b}".format(x) for x in base64Decoded])

        if(convertMethod == "base642hex"):
            hexVal = base64.b64decode(convertValue.encode()).hex()
            return " ".join([hexVal[i:i+2] for i in range(0, len(hexVal), 2)])

        if(convertMethod == "base642decimal"):
            # You need to convert each byte from the decoded string to its decimal value. Reference: https://stackoverflow.com/a/38878737
            return ' '.join([str(i) for i in base64.standard_b64decode(convertValue)])

        if(convertMethod == "base642rot13"):
            asciiVal = self.fromBase64("base642ascii", convertValue)
            rot13Val = self.fromAscii("ascii2rot13", asciiVal)
            return rot13Val
        
        if(convertMethod == "base642rot47"):
            asciiVal = self.fromBase64("base642ascii", convertValue)
            rot47Val = self.fromAscii("ascii2rot47", asciiVal)
            return rot47Val

        if(convertMethod == "base642urlencoded"):
            asciiVal = self.fromBase64("base642ascii", convertValue)
            urlFriendlyVal = self.fromAscii("ascii2urlencode", asciiVal)
            return urlFriendlyVal
        
        if(convertMethod == "base642htmlentities"):
            asciiVal = self.fromBase64("base642ascii", convertValue)
            htmlEncoded = self.fromAscii("ascii2htmlentities", asciiVal)
            return htmlEncoded


    def fromdec(self, convertMethod, convertValue):
        if(convertMethod == "decimal2ascii"):
            convertValue = self.paddingFixer(convertValue, 2)
            asciiVal = "".join([chr(int(num)) for num in [convertValue[i:i+2] for i in range(0, len(convertValue), 2)]])
            return asciiVal

        if(convertMethod == "decimal2bin"):
            pass


    def valueErrorMsg(self, convertMethod):
        layout = [
            [sg.Image(data=errorImgData, size=(350,75))],
            [sg.Text("* ERROR *", size=(290, 1), justification="center", font=("Arial", 14, "bold"), text_color="#ff4265")],
            [sg.Text("Invalid {} value detected.".format(convertMethod), size=(290, 1), justification="center", font=("Arial", 12))],
        ]
        sg.Window("Error", layout, size=(350, 175), finalize=True)


class SetupGUI():
    def __init__(self):
        
        # Setup Windows
        window = self.windowSetup()
        sgThemeGlobal = "Dark"

        # Event Loop
        while True:
            event, values = window.read()
            # print(event)  # Debug Application events & Keystroke events

            # Screen Closed
            if event in ("None", sg.WIN_CLOSED, "e:69") or "_exit_" in event:
                break


            # Theme Change
            elif(event == "Light::_light_"):
                window.close()
                window = self.windowSetup("Default1")
                sgThemeGlobal = "Default1"
                pass
            
            elif(event == "Dark::_dark_"):
                window.close()
                window = self.windowSetup()
                sgThemeGlobal = "Dark"
                pass


            # Help Tab
            elif(event == "About::_about_"):
                if(sgThemeGlobal == "Dark"):
                    layout = [
                        [sg.Image(data=aboutImgData, size=(350,75))],
                        [sg.Text("Mini Text Toolkit (MTT)", size=(290, 1), justification="center", font=("Arial", 14, "bold"), text_color="#ebd234")],
                        [sg.Text("Version 1.0", size=(290, 1), justification="center", font=("Arial", 12))],
                        [],
                        [sg.Text("Created By: ShaFdo", size=(290, 1), justification="center", font=("Arial", 12))],
                    ]
                    sg.Window("About", layout, size=(350, 200), finalize=True)
                else:
                    layout = [
                        [sg.Image(data=aboutImgData, size=(350,75))],
                        [sg.Text("Mini Text Toolkit (MTT)", size=(290, 1), justification="center", font=("Arial", 14, "bold"), text_color="#d4bf00")],
                        [sg.Text("Version 1.0", size=(290, 1), justification="center", font=("Arial", 12))],
                        [],
                        [sg.Text("Created By: ShaFdo", size=(290, 1), justification="center", font=("Arial", 12))],
                    ]
                    sg.Window("About", layout, size=(350, 200), finalize=True)


            # View History Options
            elif("_history_" in event or "h:72" in event):
                getDataDict = historyLogger().display(conn)

                getDataSortedList = sorted(getDataDict.items(), key = lambda x:datetime.strptime(x[0], '%b-%d-%Y'), reverse=True)

                content = ""

                for row in getDataSortedList:
                    content += "<div class='row'><h2>{}</h2><div class='para-wrapper'>".format(row[0])                        

                    for data in row[1]:
                        id, time, fromType, value = data
                        content += "<p><span class='green'>Time: </span> {} <br><span class='green'>Convert From: </span> {} <br> <span class='green'>Value: </span> {}</p><hr class='divider'>".format(time, fromType, value)

                    content += "</div></div>"

                historyLogger().webTempFile(tempFolderPath, content)

            elif("_historyclear_" in event):
                # Start From here
                isHistoryCleared = historyLogger().resetDB(conn)

                if(isHistoryCleared):
                    layout = [
                        [sg.Image(data=tickImgData, size=(350,100))],
                        [sg.Text("Operation Successful", size=(290, 1), justification="center", font=("Arial", 14, "bold"), text_color="#27e800" if (sgThemeGlobal == "Dark") else "#22cc00")],
                    ]
                    sg.Window("Prompt", layout, size=(350, 175), finalize=True)
                    # Continue back to the top from here
                    continue

                layout = [
                        [sg.Image(data=errorImgData, size=(350,100))],
                        [sg.Text("Operation Failed", size=(175, 1), justification="center", font=("Arial", 14, "bold"), text_color="#ff4265")],
                    ]
                
                sg.Window("Prompt", layout, size=(350, 175), finalize=True)

                
            # Clear Feilds events Options    
            elif("_clear_" in event or "r:82" in event):
                window.FindElement('_asciiTextBox_').Update('')
                window.FindElement('_binTextBox_').Update('')
                window.FindElement('_hexTextBox_').Update('')
                window.FindElement('_base64TextBox_').Update('')
                window.FindElement('_decimalTextBox_').Update('')
                window.FindElement('_rot13TextBox_').Update('')
                window.FindElement('_rot47TextBox_').Update('')
                window.FindElement('_urlEncodedTextBox_').Update('')
                window.FindElement('_htmlEntitiesTextBox_').Update('')


            # Go events
            elif("_go_" in event or "g:71" in event):
                convertor = Convertor()

                # Ascii => X
                if(len(values["_asciiTextBox_"]) > 1): 
                    val = values["_asciiTextBox_"].strip("\n")
                    historyLogger().log(conn, "ascii", val)

                    # Ascii => Bin
                    window.FindElement("_binTextBox_").Update(convertor.fromAscii("ascii2bin", val))

                    # Ascii => Hex
                    window.FindElement("_hexTextBox_").Update(convertor.fromAscii("ascii2hex", val))

                    # Ascii => Base64
                    window.FindElement("_base64TextBox_").Update(convertor.fromAscii("ascii2base64", val))

                    # Ascii => Decimal
                    window.FindElement("_decimalTextBox_").Update(convertor.fromAscii("ascii2dec", val))

                    # Ascii => Rot13
                    window.FindElement("_rot13TextBox_").Update(convertor.fromAscii("ascii2rot13", val))
                    
                    # Ascii => Rot47
                    window.FindElement("_rot47TextBox_").Update(convertor.fromAscii("ascii2rot47", val))

                    # Ascii => UrlEncode
                    window.FindElement("_urlEncodedTextBox_").Update(convertor.fromAscii("ascii2urlencode", val))

                    # Ascii => HtmlEntities
                    window.FindElement("_htmlEntitiesTextBox_").Update(convertor.fromAscii("ascii2htmlentities", val))

                # Binary => X
                elif(len(values["_binTextBox_"]) > 1): 
                    val = values["_binTextBox_"].strip("\n").replace(" ", "")
                    historyLogger().log(conn, "binary", val)

                    try:
                        # Bin => Ascii
                        window.FindElement("_asciiTextBox_").Update(convertor.fromBin("bin2ascii", val))

                        # Bin => Hex
                        window.FindElement("_hexTextBox_").Update(convertor.fromBin("bin2hex", val))

                        # Bin => Base64
                        window.FindElement("_base64TextBox_").Update(convertor.fromBin("bin2base64", val))

                        # Bin => Decimal
                        window.FindElement("_decimalTextBox_").Update(convertor.fromBin("bin2decimal", val))

                        # Bin => Rot13
                        window.FindElement("_rot13TextBox_").Update(convertor.fromBin("bin2rot13", val))

                        # Bin => Rot47
                        window.FindElement("_rot47TextBox_").Update(convertor.fromBin("bin2rot47", val))

                        # Bin => URLEncoded
                        window.FindElement("_urlEncodedTextBox_").Update(convertor.fromBin("bin2urlencode", val))

                        # Bin => HTMLEntities
                        window.FindElement("_htmlEntitiesTextBox_").Update(convertor.fromBin("bin2htmlentities", val))

                    except(ValueError):
                        convertor.valueErrorMsg("binary")

                # Hex => X
                elif(len(values["_hexTextBox_"]) > 1): 
                    val = values["_hexTextBox_"].strip("\n").replace(" ", "").replace("0x", "")
                    historyLogger().log(conn, "hex", val)

                    try:
                        # Hex => Ascii
                        window.FindElement("_asciiTextBox_").Update(convertor.fromHex("hex2ascii", val))
                        
                        # Hex => Bin
                        window.FindElement("_binTextBox_").Update(convertor.fromHex("hex2bin", val))

                        # Hex => base64
                        window.FindElement("_base64TextBox_").Update(convertor.fromHex("hex2base64", val))
                        
                        # Hex => Decimal
                        window.FindElement("_decimalTextBox_").Update(convertor.fromHex("hex2decimal", val))

                        # Hex => Rot13
                        window.FindElement("_rot13TextBox_").Update(convertor.fromHex("hex2rot13", val))

                        # Hex => Rot47
                        window.FindElement("_rot47TextBox_").Update(convertor.fromHex("hex2rot47", val))
                        
                        # Hex => URLEncoded
                        window.FindElement("_urlEncodedTextBox_").Update(convertor.fromHex("hex2urlencode", val))
                        
                        # Hex => HTMLEntities
                        window.FindElement("_htmlEntitiesTextBox_").Update(convertor.fromHex("hex2htmlentities", val))

                    except(ValueError):
                        convertor.valueErrorMsg("hex")

                # Base64 => X
                elif(len(values["_base64TextBox_"]) > 1): 
                    val = values["_base64TextBox_"].strip("\n").replace(" ", "")
                    historyLogger().log(conn, "base64", val)

                    try:
                        # Base64 => Ascii
                        window.FindElement("_asciiTextBox_").Update(convertor.fromBase64("base642ascii", val))
                        
                        # Base64 => Bin
                        window.FindElement("_binTextBox_").Update(convertor.fromBase64("base642bin", val))

                        # Base64 => Hex
                        window.FindElement("_hexTextBox_").Update(convertor.fromBase64("base642hex", val))

                        # Base64 => Decimal
                        window.FindElement("_decimalTextBox_").Update(convertor.fromBase64("base642decimal", val))

                        # Base64 => Rot13
                        window.FindElement("_rot13TextBox_").Update(convertor.fromBase64("base642rot13", val))

                        # Base64 => Rot47
                        window.FindElement("_rot47TextBox_").Update(convertor.fromBase64("base642rot47", val))
                        
                        # Base64 => UrlEncoded
                        window.FindElement("_urlEncodedTextBox_").Update(convertor.fromBase64("base642urlencoded", val))
                        
                        # Base64 => HTMLEntities
                        window.FindElement("_htmlEntitiesTextBox_").Update(convertor.fromBase64("base642htmlentities", val))

                    except(ValueError):
                        convertor.valueErrorMsg("Base64")

                # Decimal => X
                elif(len(values["_decimalTextBox_"]) > 1): 
                    val = values["_decimalTextBox_"].strip("\n").replace(" ", "")
                    historyLogger().log(conn, "decimal", val)

                    try:
                        # Decimal => Ascii
                        window.FindElement("_asciiTextBox_").Update(convertor.fromdec("decimal2ascii", val))

                        # Decimal => Binary
                        window.FindElement("_binTextBox_").Update(convertor.fromdec("decimal2bin", val))    # Start Here

                    except(ValueError):
                        convertor.valueErrorMsg("decimal")


                else:
                    layout = [
                        [sg.Image(data=errorImgData, size=(350,75))],
                        [sg.Text("* ERROR *", size=(290, 1), justification="center", font=("Arial", 14, "bold"), text_color="#ff4265")],
                        [sg.Text("No Value Detected.", size=(290, 1), justification="center", font=("Arial", 12))],
                    ]
                    sg.Window("Error", layout, size=(350, 175), finalize=True)

        window.close()
        conn.close()
        
        historyLogger().removeTempFolder(tempFolderPath)

    
    def windowSetup(self, theme="Dark"):
        darkTheme = False
        lightTheme = False
        
        # Set provided theme
        sgThemeGlobal = theme
        sg.theme(theme)
        if(theme == "Default1"): lightTheme = True
        else: darkTheme = True

        # Fonts & Colors 
        fontHeading = ("Terminal", 15)
        fontLog = ("Arial", 11, "bold")
        fontTextBox = ("Arial", 14)

        fontColors = {
            "lightColor1": "#a3a8ff",
            "lightColor2": "#ffc742",
            "lightColor3": "#00EAD3",
            "lightColor4": "#88FFF7",
            "lightColor5": "#ff7abb",
            #########################
            "darkColor1": "#4f10e0",
            "darkColor2": "#ed00d5",
            "darkColor3": "#e37900",
            "darkColor4": "#00c0c7",
            "darkColor5": "#15c21e",
            #########################
        }

        # Setup menu
        menu_stc = [
            [
                "Options", 
                [
                    "GO [Ctrl+G]::_go_",
                    "Reset Feilds [Ctrl+R]::_clear_",
                    "Theme", 
                    ["Light::_light_", "Dark::_dark_"],
                    "Exit [Ctrl+E]::_exit_",
                ],
            ],
            [
                "History",
                [
                    "View History [Ctrl+H]::_history_",
                    "Clear History ::_historyclear_",
                ]
            ],
            [
                "Help",
                [
                    "Check for updates::_update_",
                    "About::_about_",
                ]
            ]
        ]

        # Lay the stuff out accordingly
        layout = [  
            [sg.Menu(menu_stc)],

            [sg.Text('Ascii', size=(40, 1), justification="center", font=fontHeading), sg.Text('Binary', size=(40, 1), justification="center", font=fontHeading), sg.Text('Hexadecimal', size=(40, 1), justification="center", font=fontHeading)],    
            [sg.Multiline(size=(35, 7), key='_asciiTextBox_', font=fontTextBox, text_color=fontColors["lightColor5"] if(sgThemeGlobal == "Dark") else fontColors["darkColor5"]), sg.Multiline(size=(35, 7), key='_binTextBox_', font=fontTextBox, text_color=fontColors["lightColor1"] if(sgThemeGlobal == "Dark") else fontColors["darkColor1"]), sg.Multiline(size=(35, 7), key='_hexTextBox_', font=fontTextBox, text_color=fontColors["lightColor2"] if(sgThemeGlobal == "Dark") else fontColors["darkColor2"])],
            
            [sg.Text('Base64', size=(40, 1), justification="center", font=fontHeading), sg.Text('Decimal', size=(40, 1), justification="center", font=fontHeading), sg.Text('Rot13', size=(40, 1), justification="center", font=fontHeading)],    
            [sg.Multiline(size=(35, 7), key='_base64TextBox_', font=fontTextBox, text_color=fontColors["lightColor2"] if(sgThemeGlobal == "Dark") else fontColors["darkColor2"]), sg.Multiline(size=(35, 7), key='_decimalTextBox_', font=fontTextBox, text_color=fontColors["lightColor5"] if(sgThemeGlobal == "Dark") else fontColors["darkColor5"]), sg.Multiline(size=(35, 7), key='_rot13TextBox_', font=fontTextBox, text_color=fontColors["lightColor3"] if(sgThemeGlobal == "Dark") else fontColors["darkColor3"])],
            
            [sg.Text('Rot47', size=(40, 1), justification="center", font=fontHeading), sg.Text('URL Encoded', size=(40, 1), justification="center", font=fontHeading), sg.Text('HTML Entities', size=(40, 1), justification="center", font=fontHeading)],    
            [sg.Multiline(size=(35, 7), key='_rot47TextBox_', font=fontTextBox, text_color=fontColors["lightColor5"] if(sgThemeGlobal == "Dark") else fontColors["darkColor5"]), sg.Multiline(size=(35, 7), key='_urlEncodedTextBox_', font=fontTextBox, text_color=fontColors["lightColor3"] if(sgThemeGlobal == "Dark") else fontColors["darkColor3"]), sg.Multiline(size=(35, 7), key='_htmlEntitiesTextBox_', font=fontTextBox, text_color=fontColors["lightColor1"] if(sgThemeGlobal == "Dark") else fontColors["darkColor1"])],
            
            [sg.Button('GO [Ctrl+G]', size=(25, 1), key='_go_'), sg.Button('Reset Feilds [Ctrl+R]', size=(25, 1), key="_clear_")] 
        ]
            
        return sg.Window("Mini Text Toolkit (MTT)", layout, finalize=True, return_keyboard_events=True)



if (__name__ == "__main__"):
    setupgui = SetupGUI()

