from __future__ import annotations

import glob
import hashlib
import json
import os
import pathlib
import platform
import random
import subprocess
import traceback
from datetime import datetime
from threading import Thread
from tkinter import E
from tkinter import IntVar
from tkinter import Label
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import StringVar
from tkinter import Toplevel
from tkinter import ttk
from tkinter import W

import minecraft_launcher_lib as MCLib
import requests
from colorama import Fore
from colorama import init
from natsort import natsorted
from pypresence import Presence
from ttkthemes import ThemedTk

import constants
from _typing import (
    MinecraftRelease,
)

import urllib.request
import tkinter as tk
from tkinter import messagebox
import webbrowser

def check_version():
    # URL del archivo version.txt en el repositorio de GitHub
    url = 'https://raw.githubusercontent.com/acierto-incomodo/StormLauncher/master/version.txt'
    
    try:
        # Descargar el contenido del archivo version.txt
        response = urllib.request.urlopen(url)
        latest_version = response.read().decode().strip()
        
        # Obtener la versión actual del programa (puedes reemplazar esto por tu propia lógica)
        current_version = '0.0.2'
        
        # Comparar las versiones
        if current_version < latest_version:
            # Mostrar una ventana emergente con la notificación y opciones
            root = tk.Tk()
            root.withdraw()
            result = messagebox.askquestion('Actualización disponible', 'Hay una nueva versión disponible: {}. ¿Deseas actualizar?'.format(latest_version))
            
            if result == 'yes':
                # Redirigir al usuario a la página de GitHub para descargar la nueva versión
                url_github = 'https://github.com/acierto-incomodo/StormLauncher/releases/latest'
                webbrowser.open(url_github)
                
            else:
                messagebox.showinfo('Actualización cancelada', 'La actualización ha sido cancelada.')
                
            root.destroy()
            
    except Exception as e:
        # Mostrar una ventana emergente con un mensaje de error
        messagebox.showerror('Error', 'Ocurrió un error durante la verificación de la versión:\n{}'.format(str(e)))


# Ejecutar la función para verificar la versión
check_version()


ASCII = r"""
<---------------------------------------------------------------------------->
   _____ _                       _                            _              
  / ____| |                     | |                          | |
 | (___ | |_ ___  _ __ _ __ ___ | |     __ _ _   _ _ __   ___| |__   ___ _ __
  \___ \| __/ _ \| '__| '_ ` _ \| |    / _` | | | | '_ \ / __| '_ \ / _ \ '__|
  ____) | || (_) | |  | | | | | | |___| (_| | |_| | | | | (__| | | |  __/ |  
 |_____/ \__\___/|_|  |_| |_| |_|______\__,_|\__,_|_| |_|\___|_| |_|\___|_|   
  
Hecho por STORM GAMES STUDIOS

Version: V0.0.2 Alfha
<---------------------------------------------------------------------------->
"""
init()  # initialises colorama
COLOURS = (
    Fore.YELLOW,
    Fore.MAGENTA,
    Fore.BLUE,
    Fore.WHITE,
    Fore.CYAN,
    Fore.GREEN,
)
SYSTEM = platform.system()


class Config:
    # Why a class? I dont know
    Config = {}  # this is loaded later on

    Version = "V0.0.2 Alfha"
    MinecraftDir = ""

    HasInternet = True
    ShowHistorical = False


def save_config() -> None:
    """Saves the current state of the config into the file."""

    with open("config.json", "w") as f:
        json.dump(Config.Config, f, indent=4)


def log_coloured(content: str, colour: str) -> None:
    """Prints a message to the console, prefixing the message with `colour` and
    ending it with a colour reset."""

    print(colour + content + Fore.RESET)


def log_info(content: str) -> None:
    """Logs `content` to console with the severity `INFO`."""

    log_coloured(f"[{format_time()}] {content}", Fore.BLUE)


def log_warning(content: str) -> None:
    """Logs `content` to console with the severity `WARNING`."""

    log_coloured(f"[{format_time()}] {content}", Fore.YELLOW)


def log_error(content: str) -> None:
    """Logs `content` to console with the severity `ERROR`."""

    log_coloured(f"[{format_time()}] {content}", Fore.RED)


def message_box(title, content):
    """Creates a message box"""
    # MsgThread = Thread(target=ctypes.windll.user32.MessageBoxW, args=(0, content, title, style,))
    # MsgThread.start() #non blocking?
    MsgThread = Thread(
        target=messagebox.showinfo,
        args=(
            title,
            content,
        ),
    )
    MsgThread.start()
    log_info(content)


def error_box(title, content):
    """Creates an error dialogue box"""
    MsgThread = Thread(
        target=messagebox.showerror,
        args=(
            title,
            content,
        ),
    )
    MsgThread.start()
    log_error(content)


def warning_box(title, content):
    """Creater a warning dialogue box"""
    MsgThread = Thread(
        target=messagebox.showwarning,
        args=(
            title,
            content,
        ),
    )
    MsgThread.start()
    log_warning(content)


def config_window():
    """Creates an advanced config window"""
    # i know this is not supposed to be how you do it but "it just works"

    def ConfigCloseProtocol():
        """Function ran when the config window is closed"""
        ConfigWindow.destroy()
        set_default_presence()

    def SaveConfig():
        MCPath_Str = MCPath_StringVar.get()
        DRAM_Str = DRAM_StringVar.get()
        ForgetMe_Int = int(RememberMe_Var.get())

        NotFailedDRAMCheck = True

        try:
            DRAM_Str = int(DRAM_Str)
            if DRAM_Str <= 0:
                NotFailedDRAMCheck = False
        except Exception:
            NotFailedDRAMCheck = False  # nicest way i know of doing this

        if NotFailedDRAMCheck:
            if ForgetMe_Int == 1:
                Config.Config["Email"] = ""
                Config.Config["UUID"] = ""
                Config.Config["AccessToken"] = ""
                Config.Config["Username"] = ""
            Config.Config["JVMRAM"] = DRAM_Str
            if SYSTEM == "Windows":
                if MCPath_Str[-1] != "\\":
                    MCPath_Str = MCPath_Str + "\\"
            else:
                # other systems use / instead of \
                if MCPath_Str[-1] != "/":
                    MCPath_Str = MCPath_Str + "/"
            if Premium_Var.get() == 1:
                Config.Config["Premium"] = True
            if Premium_Var.get() == 0:
                Config.Config["Premium"] = False
            if Historical_Var.get() == 0:
                Config.Config["OnlyReleases"] = True
            if Historical_Var.get() == 1:
                Config.Config["OnlyReleases"] = False
            Config.Config["MinecraftDir"] = MCPath_Str
            save_config()
            config_load()  # runs config update
            ConfigWindow.destroy()
            populate_root()

        else:
            error_box(
                "StormLauncher Error!",
                "El valor de la RAM tiene que ser un numero entero (full number) sobre 0.",
            )

    # Discord Rich Presence Update
    if constants.rpc.ENABLED:
        RPC.update(
            state="Configurando cosas...",
            small_image=constants.rpc.SMALL_IMAGE,
            large_image=constants.rpc.LARGE_IMAGE,
        )
    # Initial window settings
    ConfigWindow = Toplevel(MainWindow)
    ConfigWindow.configure(background=constants.ui.BG_COLOUR)  # sets bg colour
    ConfigWindow.title("Configuracion de StormLauncher")  # sets window title
    ConfigWindow.protocol("WM_DELETE_WINDOW", ConfigCloseProtocol)
    if SYSTEM == "Windows":
        # other systems dont use ico
        MainWindow.iconbitmap(constants.ui.LOGO_ICON)  # sets window icon
    ConfigWindow.resizable(False, False)  # makes the window not resizable

    # WarningLabel
    Warning_Label = Label(
        ConfigWindow,
        text="¡Peligro! ¡Estas configuraciones son para usuarios avanzados!",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="none 12",
    )
    Warning2_Label = Label(
        ConfigWindow,
        text="¡Proceder con precaucion!",
        bg=constants.ui.BG_COLOUR,
        fg="yellow",
        font="none 12 bold",
    )
    Warning_Label.grid(row=0, column=0, sticky=W)
    Warning2_Label.grid(row=1, column=0, sticky=W)

    # MC Path Label
    MCPath_Label = Label(
        ConfigWindow,
        text="Ruta de Minecraft:",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="none 11",
    )
    MCPath_Label.grid(row=2, column=0, sticky=W)

    # MC Path Entry
    MCPath_StringVar = StringVar()
    MCPath_Entry = ttk.Entry(ConfigWindow, width=40, textvariable=MCPath_StringVar)
    MCPath_StringVar.set(Config.Config["MinecraftDir"])
    MCPath_Entry.grid(row=3, column=0, sticky=W)

    # Dedicated RAM Label
    DRAM_Label = Label(
        ConfigWindow,
        text="RAM dedicada a JVM:",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="none 11",
    )
    DRAM_Label.grid(row=4, column=0, sticky=W)

    # Dedicated RAM Entry
    DRAM_StringVar = StringVar()
    DRAM_Entry = ttk.Entry(ConfigWindow, width=10, textvariable=DRAM_StringVar)
    DRAM_StringVar.set(Config.Config["JVMRAM"])
    DRAM_Entry.grid(row=5, column=0, sticky=W)

    GB_Label = Label(
        ConfigWindow,
        text="GB",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="none 9",
    )
    GB_Label.grid(row=5, column=0, sticky=E)

    # ForgetMe RADIO
    RememberMe_Var = IntVar()  # value whether its ticked is stored here
    RememberMe_Checkbox = ttk.Checkbutton(
        ConfigWindow,
        text="Olvidarme",
        variable=RememberMe_Var,
    )
    RememberMe_Checkbox.grid(row=6, column=0, sticky=W)

    # Premium RADIO
    Premium_Var = IntVar()  # value whether its ticked is stored here
    if Config.Config["Premium"]:
        Premium_Var.set(1)  # sets to whats enabled
    Premium_Checkbox = ttk.Checkbutton(
        ConfigWindow,
        text="Usar cuenta premium de Minecraft",
        variable=Premium_Var,
    )
    Premium_Checkbox.grid(row=7, column=0, sticky=W)

    # Show Historical
    Historical_Var = IntVar()
    if not Config.Config["OnlyReleases"]:
        Historical_Var.set(1)
    Historical_Checkbox = ttk.Checkbutton(
        ConfigWindow,
        text="Mostrar versiones no lanzadas",
        variable=Historical_Var,
    )
    Historical_Checkbox.grid(row=8, column=0, sticky=W)

    # Apply Button
    Apply_Button = ttk.Button(
        ConfigWindow,
        text="Aplicar",
        width=constants.ui.BOX_WIDTH,
        command=SaveConfig,
    )
    Apply_Button.grid(row=9, column=0, sticky=W)

    # Cancel Button
    Cancel_Button = ttk.Button(
        ConfigWindow,
        text="Cancel",
        width=constants.ui.BOX_WIDTH,
        command=ConfigWindow.destroy,
    )
    Cancel_Button.grid(row=9, column=0, sticky=E)


def install(PlayAfter=False):
    """Installs minecraft"""
    # Version = "1.14.4" #later change it into a gui list # i did
    Version = ListVariable.get()

    MinecraftFound = os.path.exists(Config.MinecraftDir + f"versions\\{Version}\\")
    if MinecraftFound:
        message_box(
            "¡StormLauncher Info!",
            "¡Esta versión ya está instalada! ¡Pulsa jugar para reproducirlo!",
        )

    elif not Config.HasInternet:
        error_box(
            "¡StormLauncher Error!",
            "¡Se requiere una conexión a Internet para esta acción!",
        )

    else:
        message_box(
            "¡StormLauncher Info!",
            "¡Comenzó la descarga! Si pulsas jugar para descargar, el programa se congelará.",
        )
        callback = {
            "setStatus": set_status_handler,
            "setProgress": set_progress_handler,
            "setMax": set_max_handler,
        }
        # MCLib.install.install_minecraft_version(Version, Config.MinecraftDir, callback=callback)
        DlThread = Thread(
            target=MCLib.install.install_minecraft_version,
            args=(
                Version,
                Config.MinecraftDir,
            ),
            kwargs={"callback": callback},
        )
        DlThread.start()
        if PlayAfter:
            DlThread.join()
            play()


# TODO: Rewrite
def play():
    """Function that is done when the play button is pressed"""
    # Note 25/12/19 | Deal with sessions expiring
    def PlayRPCUpdate(version, username, isPremium):
        """Updates the rich presence so i dont have to copy and paste the same code on premium and nonpremium"""
        # Checks if the user is playing vanilla mc or modded for RPC icon
        if constants.rpc.ENABLED:
            IsVanilla = True
            MCVerList = MCLib.utils.get_version_list()
            VerList = []
            for thing in MCVerList:
                VerList.append(thing["id"])
            if version in VerList:
                IsVanilla = True
            else:
                IsVanilla = False
            if IsVanilla:
                SmallIcon = constants.rpc.VANILLA_IMAGE
            else:
                SmallIcon = constants.rpc.MODDED_IMAGE

            # Details text
            if not isPremium:
                PrState = ""
            else:
                PrState = ""
            RPC.update(
                state=f"Jugando Minecraft {version}",
                large_image=constants.rpc.LARGE_IMAGE,
                small_image=SmallIcon,
                details=f"Jugando como {username}{PrState}",
            )

    Email = Username_Entry.get()
    Password = Password_Entry.get()
    Version = ListVariable.get()
    RememberMe = RememberMe_Var.get() == 1

    # NonPremium code
    if Email == "":
        warning_box("StormLauncher Error!", "¡El nombre de usuario no puede estar vacío!")
    else:
        if Config.Config["Premium"]:
            # Attempt to make a username out of the email.
            Email, _ = Email.split("@")
        options = {
            "username": Email,
            "uuid": str(hashlib.md5(str.encode(Email)).digest()),
            "token": "",
            "launcherName": "StormLauncher",
            "gameDirectory": Config.MinecraftDir,
            "jvmArguments": [f"-Xmx{Config.Config['JVMRAM']}G"],
        }

        if RememberMe:
            Config.Config["Email"] = Email

        Config.Config["LastSelected"] = Version
        save_config()

        Command = MCLib.command.get_minecraft_command(
            Version,
            Config.MinecraftDir,
            options,
        )
        MainWindow.destroy()
        PlayRPCUpdate(Version, Email, False)

        subprocess.call(Command)
        # message_box("StormLauncher", "Thank you for using StormLauncher!") #Temporarily disabled as it would create an empty tk window


if SYSTEM == "Windows":
    MC_DIR = os.getenv("APPDATA") + "\\.minecraft\\"
else:
    # I dont know if this will work with macs or not
    MC_DIR = str(pathlib.Path.home()) + "/.minecraft/"

EXAMPLE_CONFIG = {
    "IsExample": False,
    "MinecraftDir": MC_DIR,
    "Email": "",
    "UUID": "",
    "AccessToken": "",
    "JVMRAM": 2,  # in GB
    "Premium": True,
    "LastSelected": "1.16.5",
    "OnlyReleases": True,
}

# TODO: Full rewrite.
def config_load():
    """Function to load/make new config"""
    # JSONConfig = JsonFile.GetDict("config.json")
    # if JSONConfig == {}:
    #    JSONConfig = ExampleConfig
    #    JsonFile.SaveDict(JSONConfig, "config.json")
    # if JSONConfig["IsExample"] == True:
    #    Config.Config = ExampleConfig
    # else:
    #    Config.Config = JSONConfig

    if not os.path.exists("config.json"):
        base_cfg = EXAMPLE_CONFIG.copy()
    else:
        with open("config.json") as f:
            base_cfg = json.load(f)

        if base_cfg == {}:
            base_cfg = EXAMPLE_CONFIG.copy()

    Config.Config = base_cfg

    Config.MinecraftDir = Config.Config["MinecraftDir"]

    # Making older configs compatible with newer ones
    if "JVMRAM" not in list(Config.Config.keys()):
        # for reuse of older configs
        Config.Config["JVMRAM"] = 2

    if "Premium" not in list(Config.Config.keys()):
        Config.Config["Premium"] = True

    if "LastSelected" not in list(Config.Config.keys()):
        Config.Config["LastSelected"] = "1.16.5"

    if "OnlyReleases" not in list(Config.Config.keys()):
        Config.Config["OnlyReleases"] = True
        Config.ShowHistorical = False

    # Only Releases Fixes. Not cleanest way of doing it but gets the job done
    if Config.Config["OnlyReleases"]:
        Config.ShowHistorical = False
    else:
        Config.ShowHistorical = True

    save_config()
    Config.HasInternet = check_internet()


INTERNET_TEST_URL = "https://1.1.1.1/"


def check_internet() -> bool:
    """Checks for a working internet connection"""
    try:
        resp = requests.get(INTERNET_TEST_URL, timeout=1)
        return resp.status_code == 200
    except requests.ConnectionError:
        return False


def exit_handler():
    """Function ran on the closing of the tk mainwindow"""
    MainWindow.destroy()
    exit()


def set_status_handler(status):
    Download_Progress["value"] = 0
    print(status)


def set_progress_handler(status):
    Download_Progress["value"] = int(status)


def set_max_handler(status):
    Download_Progress["maximum"] = int(status)


def get_release_list() -> list[MinecraftRelease]:
    """Returns a list of all full mc releases"""
    releases_res = requests.get(
        "https://launchermeta.mojang.com/mc/game/version_manifest.json",
    ).json()

    return [ver for ver in releases_res["versions"] if ver["type"] == "release"]


def format_time(format="%H:%M:%S") -> str:
    """Formats the current time"""
    return datetime.now().strftime(format)


def set_default_presence():
    """Sets the default presence"""
    if constants.rpc.ENABLED:
        RPC.update(
            state="En el menú principal.",
            large_image=constants.rpc.LARGE_IMAGE,
            small_image=constants.rpc.ROOT_IMAGE,
        )


def populate_root():
    """Populates the fields in this function to make the window show up faster"""
    print("Cambiando...")
    if Config.Config["Premium"]:
        Username_Label["text"] = "Correo:"
    else:
        Username_Label["text"] = "Usuario:"

    # Version list
    minecraft_versions = fetch_versions()
    minecraft_versions.insert(
        0,
        Config.Config["LastSelected"],
    )  # using a bug in ttk to our advantage
    ListVariable = StringVar(MainWindow)

    # global Ver_List
    # Ver_List = ttk.OptionMenu(MainWindow, ListVariable, *minecraft_versions)
    # Ver_List.configure(width=Config.ListLen) #only way i found of maintaining same width
    # Ver_List.grid(row=10, column=0, sticky=W)


def fetch_versions() -> list[str]:
    """Returns a list strings of all the available versions."""

    # Fetch all available releases from Mojang.
    try:
        releases = get_release_list()
    except Exception:
        log_error(
            "Failed fetching releases from web with error:\n" + traceback.format_exc(),
        )
        releases = []

    versions = [release["id"] for release in releases]

    # Fetch all currently installed versions.
    version_folders = glob.glob(Config.MinecraftDir + "versions/*/")

    for version_dir in version_folders:
        # Cursed way to fetch the version name from folder name.
        version_name = version_dir.split("\\" if SYSTEM == "Windows" else "/")[-2]
        if version_name not in versions:
            versions.append(version_name)

    # Filtering.
    for version in versions:
        # Remove betas is show historical is disabled.
        if (not Config.ShowHistorical) and version[0] == "b":
            versions.remove(version)

    # Sorting.
    versions = natsorted(versions, reverse=True)
    return versions


# The creation of the main window
if __name__ == "__main__":
    log_coloured(ASCII, random.choice(COLOURS))
    log_info("Comprobando conexion a internet...")
    config_load()
    if constants.rpc.ENABLED:
        log_info("Configurando el Rich Presence de Discord...")
        RPC = Presence(constants.rpc.CLIENT_ID)
        RPC.connect()
        set_default_presence()
    log_info("Cargando temas...")
    MainWindow = ThemedTk(theme=constants.ui.THEME)
    # Styles
    log_info("Configurando el UI...")
    s = ttk.Style()
    s.configure(
        "TButton",
        background=constants.ui.FG_COLOUR,
        fieldbackground=constants.ui.FG_COLOUR,
    )
    s.configure("TCheckbutton", background=constants.ui.BG_COLOUR, foreground="white")
    s.configure(
        "TEntry",
        fieldbackground=constants.ui.FG_COLOUR,
        background=constants.ui.FG_COLOUR,
    )

    MainWindow.configure(background=constants.ui.BG_COLOUR)  # sets bg colour
    MainWindow.title("StormLauncher")  # sets window title
    if SYSTEM == "Windows":
        # other systems dont use ico
        MainWindow.iconbitmap(constants.ui.LOGO_ICON)  # sets window icon
    MainWindow.resizable(False, False)  # makes the window not resizable
    MainWindow.protocol(
        "WM_DELETE_WINDOW",
        exit_handler,
    )  # runs the function when the user presses the X button

    # Logo Image
    StormLauncher_Logo = PhotoImage(file=constants.ui.LOGO_SMALL)
    StormLauncher_Logo_Label = Label(MainWindow, image=StormLauncher_Logo)
    StormLauncher_Logo_Label["bg"] = StormLauncher_Logo_Label.master["bg"]
    StormLauncher_Logo_Label.grid(row=0, column=0)

    # Info Label
    PInfo_Label = Label(
        MainWindow,
        text=f"StormLauncher {Config.Version}",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="Arial 15 bold",
    )
    PInfo2_Label = Label(
        MainWindow,
        text="Hecho por STORM GAMES STUDIOS",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="none 13",
    )
    PInfo_Label.grid(row=2, column=0, sticky=W)
    PInfo2_Label.grid(row=3, column=0, sticky=W)

    # Username Label
    Username_Label = Label(
        MainWindow,
        text="Correo/Usuario:",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="none 12",
    )
    Username_Label.grid(row=5, column=0, sticky=W)

    # Username Entry
    US_EntryText = StringVar()  #
    Username_Entry = ttk.Entry(
        MainWindow,
        width=constants.ui.ENTRY_LEN,
        textvariable=US_EntryText,
    )
    US_EntryText.set(Config.Config["Email"])  # inserts config email here
    Username_Entry.grid(row=6, column=0, sticky=W)

    # Password Label
    Password_Label = Label(
        MainWindow,
        text="Contraseña:",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="none 12",
    )
    Password_Label.grid(row=7, column=0, sticky=W)

    # Password Entry
    Password_Entry = ttk.Entry(MainWindow, width=constants.ui.ENTRY_LEN, show="*")
    Password_Entry.grid(row=8, column=0, sticky=W)

    # Play Button
    Play_Button = ttk.Button(
        MainWindow,
        text="¡Jugar!",
        width=constants.ui.BOX_WIDTH,
        command=play,
    )
    Play_Button.grid(row=11, column=0, sticky=W)

    # Install Button
    Install_Button = ttk.Button(
        MainWindow,
        text="¡Descargar!",
        width=constants.ui.BOX_WIDTH,
        command=install,
    )
    Install_Button.grid(row=11, column=0, sticky=E)

    # Version Label
    Version_Label = Label(
        MainWindow,
        text="Version:",
        bg=constants.ui.BG_COLOUR,
        fg="white",
        font="none 12",
    )
    Version_Label.grid(row=9, column=0, sticky=W)

    # Im just trying to get something working
    Empty = []

    ListVariable = StringVar(MainWindow)
    Ver_List = ttk.OptionMenu(MainWindow, ListVariable, *Empty)
    Ver_List.configure(
        width=constants.ui.LIST_LEN,
    )  # only way i found of maintaining same width
    Ver_List.grid(row=10, column=0, sticky=W)

    # Config Button
    Config_Button = ttk.Button(
        MainWindow,
        text="Configuracion",
        width=constants.ui.BOX_WIDTH,
        command=config_window,
    )
    Config_Button.grid(row=11, column=0)

    # Remember Me Checkbox
    RememberMe_Var = IntVar()  # value whether its ticked is stored here
    RememberMe_Checkbox = ttk.Checkbutton(
        MainWindow,
        text="Recordarme",
        variable=RememberMe_Var,
    )
    RememberMe_Checkbox.grid(row=10, column=0, sticky=E)

    # Download Progress Bar
    Download_Progress = ttk.Progressbar(MainWindow, length=constants.ui.BAR_LEN)
    Download_Progress.grid(row=12, column=0)

    minecraft_versions = fetch_versions()
    minecraft_versions.insert(
        0,
        Config.Config["LastSelected"],
    )  # using a bug in ttk to our advantage
    ListVariable = StringVar(MainWindow)
    Ver_List = ttk.OptionMenu(MainWindow, ListVariable, *minecraft_versions)
    Ver_List.configure(
        width=constants.ui.LIST_LEN,
    )  # only way i found of maintaining same width
    Ver_List.grid(row=10, column=0, sticky=W)

    log_info("¡Completado!")
    MainWindow.mainloop()
