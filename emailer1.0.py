from smtplib import SMTP_SSL as SMTP
from email.message import EmailMessage

version = "0.5, codename: 'fsociety'"

print("""
      
  _______- ___      ___       __        __    ___       _______   _______   
 /"     "||"  \    /"  |     /""\      |" \  |"  |     /"     "| /"      \  
(: ______) \   \  //   |    /    \     ||  | ||  |    (: ______)|:        | 
 \/    |   /\   \/.    |   /' /\  \    |:  | |:  |     \/    |  |_____/   ) 
 // ___)_ |: \.        |  //  __'  \   |.  |  \  |___  // ___)_  //      /  
(:      "||.  \    /:  | /   /  \   \  /\  |\( \_|:  \(:      "||:  __   \  
 \_______)|___|\__/|___|(___/    \___)(__\_|_)\_______)\_______)|__|  \___) 
                                                                            
""")
print("Simple e-mail phishing tool")
print("Version: " + version)

coms = ['help', 'show', 'use', 'exit', 'run', 'set']

optDS = {'E-mail': None,
        'Password': None,
        'SMTP': None,
        'Receiver': None}

optDM = {'E-mail': None,
        'Password': None,
        'SMTP': None,
        'Receivers(file)': None}

optM = {'Subject': None,
        'Content(file)': '',
        'Attachment': None,
        'Links:': ''}

opsD = {'email/single': optDS, 'email/mass': optDM, 'email/create': optM}

params = ['options', 'modules']
choice = ''

def help():
    print('Usage: command <module>')
    print('_______________________')
    print('Commands: ')
    for i in coms:
        print('> '+ i)
    print('Use ' + coms[4] + ' and ' + coms[5] + ' when in <module>!')
    print('Modules: ')
    for i in opsD:
        print('> '+ i)
    print("_______________________")
    print("")
    print(" To show parameters use 'show' when in <module>")
    print(" You should use 'run' to exeucute modules and save generated e-mail")
    print("""
        Write parameters correctly to set up them!
        'Content' and 'Receivers' needs .txt file""")
    
def show(inp):
    global choice
    comp = inp.split()
    if comp[1] == params[0]:
        if choice == '':
            print("Choose module to show it options!")
        else:
            for k, v in opsD[choice].items():
                print(k, v)
    elif comp[1] == params[1]:
        for i in opsD:
            print(i)
    else:
        print("Unknown argument, see 'help'")

def usemod(inp):
    global choice
    comp = inp.split()
    if comp[1] in opsD:
        choice = comp[1] 
    else:
        print("Unknown module, see 'help'")

def exitp():
    global choice
    if choice != "":
        choice = ""
    else:
        print("Bye!...")
        quit()
        
def setp():
    global choice
    comp = inp.split()
    if choice != "":
        if comp[1] in list(opsD[choice].keys()):
            opsD[choice][comp[1]] = comp[2]
        else:
            print("Option unknown, see 'show options'")
    else:
        print("Choose module! 'help'")

def mailcre():
    global choice
    global msg
    if choice != 'email/create':
        choice = 'email/create'
    print("To start sending we must create our mail first!")
    print("Change params with common commands.")
    print("After that, return to email/single or email/mass module and launch attack!")
    
def send():
    global choice
    global msg
    msg = EmailMessage()
    content = ''
    if optM['Content(file):'] != '':
        with open(optM['Content(file):'], 'r') as f:
            content_list = f.readlines()
            for i in content_list:
                content += i 
            print(content)
    msg.set_content(content + '\n' + optM['(Opt)Links:'])
    msg['Subject'] = optM['Subject:']
    msg['To'] = optDS['Receiver:']
    msg['From'] = optDS['E-mail:']
    mail = SMTP(optDS['SMTP:'])
    mail.connect(optDS['SMTP:'])
    mail.login(optDS['E-mail:'], optDS['Password:'])
    mail.sendmail(msg['From'], optDS['Receiver:'], msg.as_string())
    mail.quit()
    
def sendm():
    global choice
    global msg
    content = ''
    if optM['Content(file):'] != '':
        with open(optM['Content(file):'], 'r') as f:
            content_list = f.readlines()
            for i in content_list:
                content += i
    receivers = []
    with open(optDM['Receivers(file):'], 'r') as f:
        receivers = f.readlines()
    for r in receivers:
        msg = EmailMessage()
        msg.set_content(content + '\n' + optM['(Opt)Links:'])
        msg['Subject'] = optM['Subject:']
        msg['From'] = optDM['E-mail:']
        msg['To'] = r
        mail = SMTP(optDM['SMTP:'])
        mail.connect(optDM['SMTP:'])
        mail.login(optDM['E-mail:'], optDM['Password:'])
        mail.sendmail(optDM['E-mail:'], r, msg.as_string())
        mail.quit()
        

def run():
    global choice
    global msg
    if choice != '':
        if choice == 'email/single':
            if optM['Subject:'] == None:
                mailcre()
            else:
                send()
        elif choice == 'email/mass':
            if optM['Subject:'] == None:
                mailcre()
            else:
                sendm()
    else:
        print('Choose module first!')
        
while True:
    inp = input(choice + '> ')
    if len(inp.split()) <= 3 and len(inp.split()) > 1:
        if inp.split()[0] == 'show':
            show(inp)
        if inp.split()[0] == 'use':
            usemod(inp)
        if inp.split()[0] == 'set':
            setp()
    elif inp == 'exit':
        exitp()
    elif inp == 'help':
        help()
    elif inp == 'run':
        run()
    else:
        print("Command unknown or used incorrectly, check 'help'..")
        
