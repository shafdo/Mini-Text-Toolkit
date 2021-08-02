from calendar import c
from tkinter import font
import PySimpleGUI as sg
from urllib.parse import quote
import os, base64, codecs, html, binascii, time

# Globals
currentDir = os.path.dirname(__file__)

class Convertor():

    def toAscii(self, convertMethod, convertValue):
        if(convertMethod == "bin2ascii"):
            try:
                return binascii.unhexlify('%x' % int(str(convertValue), 2)).decode("ascii")
            except(UnicodeDecodeError):
                return "�"

            except ValueError:
                return ""

    
    def toBin(self, convertMethod, convertValue):
        if(convertMethod == "ascii2bin"):
            return ' '.join(format(ord(x), 'b') for x in convertValue)
       
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


class SetupGUI():
    def __init__(self):
        
        # Setup Windows
        window = self.windowSetup()

        # Event Loop
        while True:
            event, values = window.read()
            print(event)

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
                    [sg.Image(currentDir+"\mtt_logo.png", size=(350,50))],
                    [sg.Text("Mini Text Toolkit (MTT)", size=(290, 1), justification="center")],
                    [sg.Text("Version 1.0", size=(290, 1), justification="center")],
                    [],
                    [sg.Text("Created By: ShaFdo", size=(290, 1), justification="center")],
                ]
                sg.Window("About", layout, size=(350, 175), finalize=True)


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


            elif(event == "_go_"):
                convertor = Convertor()

                # Ascii => X
                if(len(values["_asciiTextBox_"]) > 1): 
                    val = values["_asciiTextBox_"].strip("\n")

                    # Ascii => Bin
                    window.FindElement("_binTextBox_").Update(convertor.toBin("ascii2bin", val))

                    # Ascii => Hex
                    window.FindElement("_hexTextBox_").Update(convertor.toBin("ascii2hex", val))

                    # Ascii => Base64
                    window.FindElement("_base64TextBox_").Update(convertor.toBin("ascii2base64", val))

                    # Ascii => Decimal
                    window.FindElement("_decimalTextBox_").Update(convertor.toBin("ascii2dec", val))

                    # Ascii => Rot13
                    window.FindElement("_rot13TextBox_").Update(convertor.toBin("ascii2rot13", val))
                    
                    # Ascii => Rot47
                    window.FindElement("_rot47TextBox_").Update(convertor.toBin("ascii2rot47", val))

                    # Ascii => UrlEncode
                    window.FindElement("_urlEncodedTextBox_").Update(convertor.toBin("ascii2urlencode", val))

                    # Ascii => HtmlEntities
                    window.FindElement("_htmlEntitiesTextBox_").Update(convertor.toBin("ascii2htmlentities", val))

                # Binary => X
                elif(len(values["_binTextBox_"]) > 1): 
                    val = values["_binTextBox_"].strip("\n").replace(" ", "")

                    # Bin => Ascii
                    window.FindElement("_asciiTextBox_").Update(convertor.toAscii("bin2ascii", val))  # Start Here


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
                
                [sg.Button('GO', size=(25, 1), key='_go_'), sg.Button('Reset Feilds [Ctrl+R]', size=(25, 1), key="_clear_")] 
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

                [sg.Button('GO', size=(25, 1), key='_go_'), sg.Button('Reset Feilds [Ctrl+R]', size=(25, 1), key="_clear_")] 
            ]

        return sg.Window("Mini Text Toolkit (MTT)", layout, finalize=True, return_keyboard_events=True)


setupgui = SetupGUI()

