from calendar import c
from tkinter import font
import PySimpleGUI as sg
from urllib.parse import quote
import os, base64, codecs, html, binascii, time

# Globals
currentDir = os.path.dirname(__file__)

# Icons
aboutImgData = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAACXBIWXMAAAsTAAALEwEAmpwYAAAFP0lEQVR4nO2Y7U9TVxzHGXvp9hcse7f1uaVPSQtuMxmSZWuoXUYMwqI4tbzwxabR1czE4KagYWlLl2I7kLbJeNgLN6ZbdFBELSAlS5SRLBKzFyzbMhITH0qviobffqeu19729nIv9CHc3W/yDYHb8zu/7+dezj09FRWSJEmSJEmSJEmSiiOz2bzFZDL1G43GOfTvPD1HxhgMhrfK3f+6hEFOYxBYj0mNcudYk7D5vesNn+E95c4jVC9g0wssd/MH/HkE7crjI/iZYRYAC6RmuUPxFv7vvsYSPsJ3PH4+nD2e1CxmzwUVNmxhuYsNAsY3sACoLmbPBRXebWt2AHwb2PmOx7D1LONritlzQSUKAAAVlY8m7bbkhL19KeZwC/Gt720DoRO1kOkb39qG+Y6/MfTucPb4376zDQntI9X7VbtNcPjERP2HVLw58fCXfSAGU9PNicSUvZlXeGpqWxM189FKuZsuOATMlLj23o7VAVxvus8YPNOC3rVB3ZL9JNzjDP94qn77s9C7gbr2DiRHTbA0atjQTkbNqSwkUwpCrH47x+P/wRihlrxcXfbGCw4CM5Fs1FRDND8AXPiSV98ue7NFg3ClNrUgsoZ/MG1XUTM7y95ksU0yJsZtmhwAySlHX3JyW9kbLPpTgBmpSUdvDoCH041/Jq9sKXuDRQeAGSnMyggPP9dtouK7VpZGjbwL3R8xw4+Rw9B/9jRMDu4ueZDY4B74pvcUXIgcggdC3lZRE1DxlhWYsL9MAzi23+I62lp958BO7Xw+H26pmh84rr6TdtDtWg6Hw5ByKAR97fZE+lrvUc0iV621uPczzWK6fl+7I0HPjf7a/elyZm+HWrS3uWqRrMf2V7toAHK5/JRMJgMuW0wyuPjl67R7zrghs4mw72P62qhHzllrLR7Bmun64a5PGHP3BNyM3qym1efHzB00AK1Wu1U4AA+jiZDvQOkA+A4y5u4NeAUDwMy1mcvAi2q1+qlOp4N83mzVwe0hDe2g73Po7u6mPfiVk742EdDkrbNWx848n3vQ38qYm/SS2dtmC3ctlUr1lGRmLIRI5G+ug8k3apgLpL/DCW1tbbTP+x30tZk+Q6EOQ2nHzz6f+7z/fcbc/o5WRm9v1nDXwqx/5bwG8Y+z6wFwobuUABzrBXAzB4BGo4kKARDqbGI0Md6ztWQALvfUMeYOde4QCmCEDcCQEACxgB48Xzih/bgLgu2NMD+gKRmAW/1qCJxshJM4t/eEE9cHvSAAmHUgBwAugl1CANwMqxgr7x/ndCUDsHBOy5h7NqLiDcBoNAJmdecAwJXRSS7yBXD3oh6mg0oY88rg14iaca3YAIhn8QaQueNBBdy9xP8JMBgMBMDeHABVVVV6NG8AXC4FAC5zAdDr9cRVOQBQlfiOXBY7AMz4mGRlA8C5FxALANY9QAaAvHsBEQHI3QOkxbUXEBGA3D1ABoBBsQMgGbkAeMUMgLzmMaMnLwDcC+zLtxcQCwDWPUBaXHsBMQAg2fLtAdKqxEWCdS8gBgCce4CMdWBRrADw5v7DGf6/dYB1MyQGACQbHwBzaNEBIJmUSuUcHwBecmiIH059cUi/FTYiANI7yUCykEysX4NZALykUCgeZRwfA/4OVrMCxn1yXh7rUqTGFNLRLiXv+avNytQY0ns6B8mEi+CmVQEQ4UJYh4OecB2Lc7nYx+KrOftYHEE8IUf/vMKnhY/Lq/g0jCC5e1hg2WKQL0c9MuDjnzoVK2RMIU1q8p3fan42hvSOGS7h+/8VQeElSZIkSZIkSZL+D/oXjKMfxw94DhgAAAAASUVORK5CYII='
errorImgData = b'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'

class Convertor():

    def fromAscii(self, convertMethod, convertValue):
        if(convertMethod == "ascii2bin"):
            return "0" +' 0'.join(format(ord(x), 'b') for x in convertValue)
       
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
                return binascii.unhexlify('%x' % int(str(convertValue), 2)).decode("ascii")
            except(UnicodeDecodeError):
                return "�"

            except ValueError:
                return ""

        if(convertMethod == "bin2hex"):
            hexValWithout0x = hex(int(convertValue, 2))[2:]
            hexValSpaceInBetween = " ".join([hexValWithout0x[i:i+2] for i in range(0, len(hexValWithout0x), 2)])
            return hexValSpaceInBetween

        if(convertMethod == "bin2base64"):
            getAscii = self.fromBin("bin2ascii", convertValue)
            return base64.b64encode(getAscii.encode()).decode("utf-8")

        if(convertMethod == "bin2decimal"):
            decimalNumContainer = []
            if(len(convertValue) % 8 == 0):
                # 8 bit padding ok
                valuesSplitBy8 = [convertValue[i:i+8] for i in range(0, len(convertValue), 8)]
                for val in valuesSplitBy8: decimalNumContainer.append(int(val, 2))
                temp = [str(val) for val in decimalNumContainer]
                return " ".join(temp)

            else:
                # 8 bit Padding incorrect {MUST FIX PADDING}
                allBinaryChars = [i for i in convertValue]
                bit8SplitContainer = []

                while 1:
                    if(len(allBinaryChars) == 0): break
                    
                    elif(len(allBinaryChars) >= 8):
                        bit8SplitContainer.append("".join(allBinaryChars[:8]))
                        del allBinaryChars[:8]

                    else: allBinaryChars.insert(0, "0")

                return self.fromBin("bin2decimal", "".join(bit8SplitContainer))


        if(convertMethod == "bin2rot13"):
            asciiVal = self.fromBin("bin2ascii", convertValue)
            rot13Val = self.fromAscii("ascii2rot13", asciiVal)
            return rot13Val

        if(convertMethod == "bin2rot47"):
            asciiVal = self.fromBin("bin2ascii", convertValue)
            rot47Val = self.fromAscii("ascii2rot47", asciiVal)
            return rot47Val

                




class SetupGUI():
    def __init__(self):
        
        # Setup Windows
        window = self.windowSetup()

        # Event Loop
        while True:
            event, values = window.read()
            # print(event)

            # Screen Closed
            if event in ("None", sg.WIN_CLOSED, "e:69") or "_exit_" in event:
                break


            # Theme Change
            elif(event == "Light::_light_"):
                window.close()
                window = self.windowSetup("Default1")
                pass
            

            elif(event == "Dark::_dark_"):
                window.close()
                window = self.windowSetup()
                pass


            # Help Options
            elif(event == "About::_about_"):
                layout = [
                    [sg.Image(data=aboutImgData, size=(350,75))],
                    [sg.Text("Mini Text Toolkit (MTT)", size=(290, 1), justification="center")],
                    [sg.Text("Version 1.0", size=(290, 1), justification="center")],
                    [],
                    [sg.Text("Created By: ShaFdo", size=(290, 1), justification="center")],
                ]
                sg.Window("About", layout, size=(350, 200), finalize=True)


            # Go and Clear btn events          
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


            elif(event == "_go_" or "g:71" in event):
                convertor = Convertor()

                # Ascii => X
                if(len(values["_asciiTextBox_"]) > 1): 
                    val = values["_asciiTextBox_"].strip("\n")

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
                    window.FindElement("_urlEncodedTextBox_").Update(convertor.fromBin("bin2urlencode", val))   # Start Here

                else:
                    layout = [
                        [sg.Image(data=errorImgData, size=(350,75))],
                        [sg.Text("ERROR", size=(290, 1), justification="center")],
                        [sg.Text("No Value Detected.", size=(290, 1), justification="center")],
                    ]
                    sg.Window("Error", layout, size=(350, 175), finalize=True)

        window.close()

    
    def windowSetup(self, theme="Dark"):
        darkTheme = False
        lightTheme = False
        
        # Set provided theme
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
                    "Reset Feilds [Ctrl+R]::_clear_",
                    "Theme", 
                    ["Light::_light_", "Dark::_dark_"],
                    "Exit [Ctrl+E]::_exit_",
                ],
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
        if darkTheme == True:
            layout = [  
                [sg.Menu(menu_stc)],

                [sg.Text('Ascii', size=(40, 1), justification="center", font=fontHeading), sg.Text('Binary', size=(40, 1), justification="center", font=fontHeading), sg.Text('Hexadecimal', size=(40, 1), justification="center", font=fontHeading)],    
                [sg.Multiline(size=(35, 7), key='_asciiTextBox_', font=fontTextBox, text_color=fontColors["lightColor5"]), sg.Multiline(size=(35, 7), key='_binTextBox_', font=fontTextBox, text_color=fontColors["lightColor1"]), sg.Multiline(size=(35, 7), key='_hexTextBox_', font=fontTextBox, text_color=fontColors["lightColor2"])],
                
                [sg.Text('Base64', size=(40, 1), justification="center", font=fontHeading), sg.Text('Decimal', size=(40, 1), justification="center", font=fontHeading), sg.Text('Rot13', size=(40, 1), justification="center", font=fontHeading)],    
                [sg.Multiline(size=(35, 7), key='_base64TextBox_', font=fontTextBox, text_color=fontColors["lightColor2"]), sg.Multiline(size=(35, 7), key='_decimalTextBox_', font=fontTextBox, text_color=fontColors["lightColor5"]), sg.Multiline(size=(35, 7), key='_rot13TextBox_', font=fontTextBox, text_color=fontColors["lightColor3"])],
                
                [sg.Text('Rot47', size=(40, 1), justification="center", font=fontHeading), sg.Text('URL Encoded', size=(40, 1), justification="center", font=fontHeading), sg.Text('HTML Entities', size=(40, 1), justification="center", font=fontHeading)],    
                [sg.Multiline(size=(35, 7), key='_rot47TextBox_', font=fontTextBox, text_color=fontColors["lightColor5"]), sg.Multiline(size=(35, 7), key='_urlEncodedTextBox_', font=fontTextBox, text_color=fontColors["lightColor3"]), sg.Multiline(size=(35, 7), key='_htmlEntitiesTextBox_', font=fontTextBox, text_color=fontColors["lightColor1"])],
                
                [sg.Button('GO [Ctrl+G]', size=(25, 1), key='_go_'), sg.Button('Reset Feilds [Ctrl+R]', size=(25, 1), key="_clear_")] 
            ]
        
        else:
            layout = [  
                [sg.Menu(menu_stc)],
                
                [sg.Text('Ascii', size=(40, 1), justification="center", font=fontHeading), sg.Text('Binary', size=(40, 1), justification="center", font=fontHeading), sg.Text('Hexadecimal', size=(40, 1), justification="center", font=fontHeading)],    
                [sg.Multiline(size=(35, 7), key='_asciiTextBox_', font=fontTextBox, text_color=fontColors["darkColor5"]), sg.Multiline(size=(35, 7), key='_binTextBox_', font=fontTextBox, text_color=fontColors["darkColor1"]), sg.Multiline(size=(35, 7), key='_hexTextBox_', font=fontTextBox, text_color=fontColors["darkColor2"])],
                
                [sg.Text('Base64', size=(40, 1), justification="center", font=fontHeading), sg.Text('Decimal', size=(40, 1), justification="center", font=fontHeading), sg.Text('Rot13', size=(40, 1), justification="center", font=fontHeading)],    
                [sg.Multiline(size=(35, 7), key='_base64TextBox_', font=fontTextBox, text_color=fontColors["darkColor2"]), sg.Multiline(size=(35, 7), key='_decimalTextBox_', font=fontTextBox, text_color=fontColors["darkColor5"]), sg.Multiline(size=(35, 7), key='_rot13TextBox_', font=fontTextBox, text_color=fontColors["darkColor3"])],
                
                [sg.Text('Rot47', size=(40, 1), justification="center", font=fontHeading), sg.Text('URL Encoded', size=(40, 1), justification="center", font=fontHeading), sg.Text('HTML Entities', size=(40, 1), justification="center", font=fontHeading)],    
                [sg.Multiline(size=(35, 7), key='_rot47TextBox_', font=fontTextBox, text_color=fontColors["darkColor5"]), sg.Multiline(size=(35, 7), key='_urlEncodedTextBox_', font=fontTextBox, text_color=fontColors["darkColor3"]), sg.Multiline(size=(35, 7), key='_htmlEntitiesTextBox_', font=fontTextBox, text_color=fontColors["darkColor1"])],
                
                [sg.Text("spacer", visible=False)],

                [sg.Button('GO [Ctrl+G]', size=(25, 1), key='_go_'), sg.Button('Reset Feilds [Ctrl+R]', size=(25, 1), key="_clear_")] 
            ]

        return sg.Window("Mini Text Toolkit (MTT)", layout, finalize=True, return_keyboard_events=True)


setupgui = SetupGUI()

