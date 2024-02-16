from functions import *

#generate_key()

clr()
key = str(input("SECRET KEY: "))

if key:

    while True:
        print(Fore.GREEN + "[PASSWORD " + Fore.YELLOW + "MANAGER " + Fore.RED + "ONLINE]" + Style.RESET_ALL)

        print("""
        [DEVELOPED BY: Tomás Neto in 2024]\n\n
        1 - ADD ACCOUNT\n
        2 - SEE ACCOUNT\n
        3 - UPDATE ACCOUNT\n
        4 - DELETE ACCOUNT\n\n
        5 - CLEAN SCREEN\n
        0 - QUIT\n

        """)

        cmd = input("> ")

        if cmd == '1':
            clr()
            insertAccount(key)
            clr()

        elif cmd == '2':
            clr()
            viewAccount(key)
        

        elif cmd == '3':
            clr()
            updateAccount(key)
            clr()

        elif cmd == '4':
            clr()
            deleteAccount()
            clr()

        elif cmd == '5':
            clr()

        else:
            clr()
            print(Fore.GREEN + "DATA BASE CLOSED!" + Style.RESET_ALL)
            break

else:
    print(Fore.RED + "\nERROR: No key inserted." + Style.RESET_ALL)