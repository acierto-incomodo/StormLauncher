#RealistikDash here, just be careful and wear eye protection while looking at this
from threading import Thread
from tkinter import *
from tkinter import ttk, messagebox
from natsort import natsorted
from colorama import init, Fore
from datetime import datetime
from pypresence import Presence
from ttkthemes import ThemedTk
from _typing import (
    MinecraftRelease,
)
import minecraft_launcher_lib as MCLib
import subprocess
import os
import json
import hashlib
import requests
import platform
import pathlib
import random
import traceback
import glob

ASCII = """ _____       __  __       __  __  _____ 
 |  __ \     |  \/  |     |  \/  |/ ____|
 | |__) |   _| \  / |_   _| \  / | |     
 |  ___/ | | | |\/| | | | | |\/| | |     
 | |   | |_| | |  | | |_| | |  | | |____ 
 |_|    \__, |_|  |_|\__, |_|  |_|\_____|
         __/ |        __/ |              
        |___/        |___/   by RealistikDash
"""
init() #initialises colorama
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
    #Why a class? I dont know
    Config = {} # this is loaded later on

    Version = "0.1.8MC"
    MinecraftDir = ""

    BG_Colour = '#2F3136'
    FG_Colour = "#2c3e50"
    Theme = "equilux"

    HasInternet = True
    ShowHistorical = False

    #Discord Rich Presence Settings
    RPCEnable = False
    ClientId = "673338815301287966"
    LargeImage = "pymymc_logo"
    ConfigImage = "config"
    RootImage = "main"
    VanillaImage = "vanilla"
    ModdedImage = "modded"

    #More advanced options
    # If set to true, the System ver will be set to "Linux" to help test things. That variable is used by PyMyMC
    # to check what OS the user is using (eg Windows, Linux, MacOS/Darwin)
    FakeLinux = False 
    if FakeLinux:
        #done in the class so the later on code isnt broken
        global SYSTEM
        SYSTEM = "Linux"

    #GUI properties for different systems
    ## On some systems (namely linux) widget size would be way different than on my 
    ## development environment (Windows) so this part of the code makes sure things
    ## look at least similar on most major systems.
    if SYSTEM == "Windows":
        BoxWidth = 10
        EntryLen = 40
        BarLen = 245
        ListLen = 15
    else:
        BoxWidth = 7
        EntryLen = 30
        BarLen = 245
        ListLen = 8

def save_config() -> None:
    """Saves the current state of the config into the file."""

    with open("config.json", "w") as f:
        json.dump(Config.Config, f, indent= 4)

class Path:
    #class to store file paths, made for easy and quick changes
    if SYSTEM == "Windows":
        Logo_Small = "img\\pymymc_logo_small.png"
        Logo_Icon = "img\\pymymc_ico.ico"
    else:
        Logo_Small = "img/pymymc_logo_small.png"
        Logo_Icon = "img/pymymc_logo_small.png"

def log_coloured(content: str, colour: str) -> None:
    """Prints a message to the console, prefixing the message with `colour` and
    ending it with a colour reset."""

    print(colour + content + Fore.RESET)

def log_info(content: str) -> None:
    """Logs `content` to console with the severity `INFO`."""

    log_coloured(f"[{FormatTime()}] {content}", Fore.BLUE)

def log_warning(content: str) -> None:
    """Logs `content` to console with the severity `WARNING`."""

    log_coloured(f"[{FormatTime()}] {content}", Fore.YELLOW)

def log_error(content: str) -> None:
    """Logs `content` to console with the severity `ERROR`."""

    log_coloured(f"[{FormatTime()}] {content}", Fore.RED)

def MessageBox(title, content):
    """Creates a message box"""
    #MsgThread = Thread(target=ctypes.windll.user32.MessageBoxW, args=(0, content, title, style,))
    #MsgThread.start() #non blocking?
    MsgThread = Thread(target=messagebox.showinfo, args=(title, content,))
    MsgThread.start()
    log_info(content)

def ErrorBox(title, content):
    """Creates an error dialogue box"""
    MsgThread = Thread(target=messagebox.showerror, args=(title, content,))
    MsgThread.start()
    log_error(content)

def WarningBox(title, content):
    """Creater a warning dialogue box"""
    MsgThread = Thread(target=messagebox.showwarning, args=(title, content,))
    MsgThread.start()
    log_warning(content)

def ConfigWindowFunc():
    """Creates an advanced config window"""
    #i know this is not supposed to be how you do it but "it just works"

    def ConfigCloseProtocol():
        """Function ran when the config window is closed"""
        ConfigWindow.destroy()
        DefaultPresence()

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
            NotFailedDRAMCheck = False #nicest way i know of doing this

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
                #other systems use / instead of \
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
            ConfigLoad() #runs config update
            ConfigWindow.destroy()
            PopulateRoot()
        
        
        else:
            ErrorBox("PyMyMC Error!", "The RAM value has to be an integer (full number) over 0.")

    #Discord Rich Presence Update
    if Config.RPCEnable:
        RPC.update(state="Configuring things...", small_image=Config.ConfigImage, large_image=Config.LargeImage)
    #Initial window settings
    ConfigWindow = Toplevel(MainWindow)
    ConfigWindow.configure(background=Config.BG_Colour) # sets bg colour
    ConfigWindow.title("PyMyMC Config") # sets window title
    ConfigWindow.protocol("WM_DELETE_WINDOW", ConfigCloseProtocol)
    if SYSTEM == "Windows":
        #other systems dont use ico
        MainWindow.iconbitmap(Path.Logo_Icon) # sets window icon
    ConfigWindow.resizable(False, False) #makes the window not resizable

    #WarningLabel
    Warning_Label = Label(ConfigWindow, text="Warning! These options are for advanced users only!", bg = Config.BG_Colour, fg = "white", font = "none 12")
    Warning2_Label = Label(ConfigWindow, text="Proceed with caution!", bg = Config.BG_Colour, fg = "yellow", font = "none 12 bold")
    Warning_Label.grid(row=0, column=0, sticky=W)
    Warning2_Label.grid(row=1, column=0, sticky=W)

    #MC Path Label
    MCPath_Label = Label(ConfigWindow, text="Minecraft Path:", bg = Config.BG_Colour, fg = "white", font = "none 11")
    MCPath_Label.grid(row=2, column=0, sticky=W)

    #MC Path Entry
    MCPath_StringVar = StringVar()
    MCPath_Entry = ttk.Entry(ConfigWindow, width=40, textvariable=MCPath_StringVar)
    MCPath_StringVar.set(Config.Config["MinecraftDir"])
    MCPath_Entry.grid(row=3, column=0, sticky=W)

    #Dedicated RAM Label
    DRAM_Label = Label(ConfigWindow, text="JVM Dedicated RAM:", bg = Config.BG_Colour, fg = "white", font = "none 11")
    DRAM_Label.grid(row=4,column=0,sticky=W) 

    #Dedicated RAM Entry
    DRAM_StringVar = StringVar()
    DRAM_Entry = ttk.Entry(ConfigWindow, width=10, textvariable=DRAM_StringVar)
    DRAM_StringVar.set(Config.Config["JVMRAM"])
    DRAM_Entry.grid(row=5, column=0, sticky=W)

    GB_Label = Label(ConfigWindow, text="GB", bg = Config.BG_Colour, fg = "white", font = "none 9")
    GB_Label.grid(row=5, column=0, sticky=E)

    #ForgetMe RADIO
    RememberMe_Var = IntVar() #value whether its ticked is stored here
    RememberMe_Checkbox = ttk.Checkbutton(ConfigWindow, text="Forget Me", variable=RememberMe_Var)
    RememberMe_Checkbox.grid(row=6, column=0, sticky=W)

    #Premium RADIO
    Premium_Var = IntVar() #value whether its ticked is stored here
    if Config.Config["Premium"]:
        Premium_Var.set(1) #sets to whats enabled
    Premium_Checkbox = ttk.Checkbutton(ConfigWindow, text="Use Premium Minecraft Accounts", variable=Premium_Var)
    Premium_Checkbox.grid(row=7, column=0, sticky=W)

    #Show Historical
    Historical_Var = IntVar()
    if not Config.Config["OnlyReleases"]:
        Historical_Var.set(1)
    Historical_Checkbox = ttk.Checkbutton(ConfigWindow, text="Show non-release versions", variable=Historical_Var)
    Historical_Checkbox.grid(row=8, column=0, sticky=W)
    
    #Apply Button
    Apply_Button = ttk.Button(ConfigWindow, text="Apply", width=Config.BoxWidth, command = SaveConfig)
    Apply_Button.grid(row=9, column=0, sticky=W)

    #Cancel Button
    Cancel_Button = ttk.Button(ConfigWindow, text="Cancel", width=Config.BoxWidth, command = ConfigWindow.destroy)
    Cancel_Button.grid(row=9, column=0, sticky=E)

def Install(PlayAfter = False):
    """Installs minecraft"""
    #Version = "1.14.4" #later change it into a gui list # i did
    Version = ListVariable.get()

    MinecraftFound = os.path.exists(Config.MinecraftDir+f"versions\\{Version}\\")
    if MinecraftFound:
        MessageBox("PyMyMC Info!", "This version is already installed! Press play to play it!")

    elif not Config.HasInternet:
        ErrorBox("PyMyMC Error!", "An internet connection is required for this action!")

    else:
        MessageBox("PyMyMC Info!", "Downloading started! If you pressed play to download, the program will freeze.")
        callback = {
            "setStatus": SetStatusHandler,
            "setProgress" : SetProgressHandler,
            "setMax": SetMaxHandler,
        }
        #MCLib.install.install_minecraft_version(Version, Config.MinecraftDir, callback=callback)
        DlThread = Thread(target=MCLib.install.install_minecraft_version, args=(Version, Config.MinecraftDir,), kwargs={"callback" : callback})
        DlThread.start()
        if PlayAfter:
            DlThread.join()
            Play()

# TODO: Rewrite
def Play():
    """Function that is done when the play button is pressed"""
    #Note 25/12/19 | Deal with sessions expiring
    def PlayRPCUpdate(version, username, isPremium):
        """Updates the rich presence so i dont have to copy and paste the same code on premium and nonpremium"""
        #Checks if the user is playing vanilla mc or modded for RPC icon
        if Config.RPCEnable:
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
                SmallIcon = Config.VanillaImage
            else:
                SmallIcon = Config.ModdedImage

            #Details text
            if not isPremium:
                PrState = ", non-premuim"
            else:
                PrState = ""
            RPC.update(
                state=f"Playing Minecraft {version}",
                large_image=Config.LargeImage,
                small_image=SmallIcon,
                details=f"Playing as {username}{PrState}"
            )


    Email = Username_Entry.get()
    Password = Password_Entry.get()
    Version = ListVariable.get()
    RememberMe = RememberMe_Var.get() == 1

    #NonPremium code
    if Email == "":
        WarningBox("PyMyMC Error!", "Username cannot be empty!")
    else:
        if Config.Config["Premium"]:
            # Attempt to make a username out of the email.
            Email, _ = Email.split("@")
        options = {
            "username" : Email,
            "uuid" : str(hashlib.md5(str.encode(Email)).digest()),
            "token" : "",
            "launcherName": "PyMyMC",
            "gameDirectory": Config.MinecraftDir,
            "jvmArguments" : [f"-Xmx{Config.Config['JVMRAM']}G"]
        }

        if RememberMe:
            Config.Config["Email"] = Email

        Config.Config["LastSelected"] = Version
        save_config()
        
        Command = MCLib.command.get_minecraft_command(Version, Config.MinecraftDir, options)
        MainWindow.destroy()
        PlayRPCUpdate(Version, Email, False)
        
        subprocess.call(Command)
        #MessageBox("PyMyMC", "Thank you for using PyMyMC!") #Temporarily disabled as it would create an empty tk window

if SYSTEM == "Windows":
    MC_DIR = os.getenv('APPDATA') + "\\.minecraft\\"
else:
    #I dont know if this will work with macs or not
    MC_DIR = str(pathlib.Path.home()) + "/.minecraft/"

EXAMPLE_CONFIG = {
        "IsExample" : False,
        "MinecraftDir" : MC_DIR,
        "Email" : "",
        "UUID" : "",
        "AccessToken" : "",
        "JVMRAM" : 2, #in GB
        "Premium" : True,
        "LastSelected" : "1.15.1",
        "OnlyReleases" : True,
    }

# TODO: Full rewrite.
def ConfigLoad():
    """Function to load/make new config"""
    #JSONConfig = JsonFile.GetDict("config.json")
    #if JSONConfig == {}:
    #    JSONConfig = ExampleConfig
    #    JsonFile.SaveDict(JSONConfig, "config.json")
    #if JSONConfig["IsExample"] == True:
    #    Config.Config = ExampleConfig
    #else:
    #    Config.Config = JSONConfig

    if not os.path.exists("config.json"):
        base_cfg = EXAMPLE_CONFIG.copy()
    else:
        with open("config.json", "r") as f:
            base_cfg = json.load(f)
        
        if base_cfg == {}:
            base_cfg = EXAMPLE_CONFIG.copy()
    
    Config.Config = base_cfg

    Config.MinecraftDir = Config.Config["MinecraftDir"]  

    #Making older configs compatible with newer ones
    if "JVMRAM" not in list(Config.Config.keys()):
        #for reuse of older configs
        Config.Config["JVMRAM"] = 2
    
    if "Premium" not in list(Config.Config.keys()):
        Config.Config["Premium"] = True

    if "LastSelected" not in list(Config.Config.keys()):
        Config.Config["LastSelected"] = "1.15.1"
    
    if "OnlyReleases" not in list(Config.Config.keys()):
        Config.Config["OnlyReleases"] = True
        Config.ShowHistorical = False

    #Only Releases Fixes. Not cleanest way of doing it but gets the job done
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

def ExitHandler():
    """Function ran on the closing of the tk mainwindow"""
    MainWindow.destroy()
    exit()

def SetStatusHandler(status):
    Download_Progress["value"] = 0
    print(status)

def SetProgressHandler(status):
    Download_Progress["value"] = int(status)
    

def SetMaxHandler(status):
    Download_Progress["maximum"] = int(status)

def get_release_list() -> list[MinecraftRelease]:
    """Returns a list of all full mc releases"""
    releases_res = requests.get(
        "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    ).json()
    
    return [ver for ver in releases_res["versions"] if ver["type"] == "release"]

def FormatTime(format="%H:%M:%S") -> str:
    """Formats the current time"""
    return datetime.now().strftime(format)

def DefaultPresence():
    """Sets the default presence"""
    if Config.RPCEnable:
        RPC.update(
            state= "In the main menu.",
            large_image= Config.LargeImage,
            small_image= Config.RootImage
        )

def PopulateRoot():
    """Populates the fields in this function to make the window show up faster"""
    print("Populating...")
    if Config.Config["Premium"]:
        Username_Label["text"] = "Email"
    else:
        Username_Label["text"] = "Username:"
    
    #Version list
    minecraft_versions = fetch_versions()
    minecraft_versions.insert(0, Config.Config["LastSelected"]) #using a bug in ttk to our advantage
    ListVariable = StringVar(MainWindow)
    
    #global Ver_List
    #Ver_List = ttk.OptionMenu(MainWindow, ListVariable, *minecraft_versions)
    #Ver_List.configure(width=Config.ListLen) #only way i found of maintaining same width
    #Ver_List.grid(row=10, column=0, sticky=W)

def fetch_versions() -> list[str]:
    """Returns a list strings of all the available versions."""

    # Fetch all available releases from Mojang.
    try:
        releases = get_release_list()
    except Exception:
        log_error("Failed fetching releases from web with error:\n"
                    + traceback.format_exc())
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
    versions = natsorted(versions, reverse= True)
    return versions

#The creation of the main window
if __name__ == '__main__':
    log_coloured(ASCII, random.choice(COLOURS))
    log_info("Checking internet status...")
    ConfigLoad()
    if Config.RPCEnable:
        log_info("Configuring the Discord Rich Presence...")
        RPC = Presence(Config.ClientId)
        RPC.connect()
        DefaultPresence()
    log_info("Loading themes...")
    MainWindow = ThemedTk(theme=Config.Theme)
    #Styles
    log_info("Configuring the UI...")
    s = ttk.Style()
    s.configure('TButton', background=Config.FG_Colour, fieldbackground=Config.FG_Colour)
    s.configure('TCheckbutton', background=Config.BG_Colour, foreground="white")
    s.configure('TEntry', fieldbackground=Config.FG_Colour, background=Config.FG_Colour)

    MainWindow.configure(background=Config.BG_Colour) # sets bg colour
    MainWindow.title("PyMyMC") # sets window title
    if SYSTEM == "Windows":
        #other systems dont use ico
        MainWindow.iconbitmap(Path.Logo_Icon) # sets window icon
    MainWindow.resizable(False, False) #makes the window not resizable
    MainWindow.protocol("WM_DELETE_WINDOW", ExitHandler) #runs the function when the user presses the X button

    #Logo Image
    PyMyMC_Logo = PhotoImage(file=Path.Logo_Small)
    PyMyMC_Logo_Label = Label(MainWindow, image=PyMyMC_Logo)
    PyMyMC_Logo_Label['bg'] = PyMyMC_Logo_Label.master['bg']
    PyMyMC_Logo_Label.grid(row=0, column=0) 

    #Info Label
    PInfo_Label = Label(MainWindow, text=f"PyMyMC {Config.Version}", bg=Config.BG_Colour, fg = 'white', font = "Arial 15 bold")
    PInfo2_Label = Label(MainWindow, text="Made by RealistikDash", bg=Config.BG_Colour, fg = 'white', font = "none 13")
    PInfo_Label.grid(row=2, column=0, sticky=W)
    PInfo2_Label.grid(row=3, column=0, sticky=W)

    #Username Label
    Username_Label = Label(MainWindow, text="Email:", bg = Config.BG_Colour, fg = "white", font = "none 12")
    Username_Label.grid(row=5, column=0, sticky=W)

    #Username Entry
    US_EntryText = StringVar() #
    Username_Entry = ttk.Entry(MainWindow, width=Config.EntryLen, textvariable=US_EntryText)
    US_EntryText.set(Config.Config["Email"]) #inserts config email here
    Username_Entry.grid(row=6, column = 0, sticky=W)

    #Password Label
    Password_Label = Label(MainWindow, text="Password:", bg = Config.BG_Colour, fg = "white", font = "none 12")
    Password_Label.grid(row=7, column=0, sticky=W)

    #Password Entry
    Password_Entry = ttk.Entry(MainWindow, width=Config.EntryLen, show="*")
    Password_Entry.grid(row=8, column = 0, sticky=W)

    #Play Button
    Play_Button = ttk.Button(MainWindow, text="Play!", width=Config.BoxWidth, command = Play)
    Play_Button.grid(row = 11, column=0, sticky = W)

    #Install Button
    Install_Button = ttk.Button(MainWindow, text="Download!", width=Config.BoxWidth, command = Install)
    Install_Button.grid(row = 11, column=0, sticky = E)

    #Version Label
    Version_Label = Label(MainWindow, text="Version:", bg = Config.BG_Colour, fg = "white", font = "none 12")
    Version_Label.grid(row=9, column=0, sticky=W)

    #Im just trying to get something working
    Empty = []

    ListVariable = StringVar(MainWindow)
    Ver_List = ttk.OptionMenu(MainWindow, ListVariable, *Empty)
    Ver_List.configure(width=Config.ListLen) #only way i found of maintaining same width
    Ver_List.grid(row=10, column=0, sticky=W)

    #Config Button
    Config_Button = ttk.Button(MainWindow, text="Config",  width=Config.BoxWidth, command = ConfigWindowFunc)
    Config_Button.grid(row = 11, column=0)

    #Remember Me Checkbox
    RememberMe_Var = IntVar() #value whether its ticked is stored here
    RememberMe_Checkbox = ttk.Checkbutton(MainWindow, text="Remember me", variable=RememberMe_Var)
    RememberMe_Checkbox.grid(row=10, column=0, sticky=E)

    #Download Progress Bar
    Download_Progress = ttk.Progressbar(MainWindow, length=Config.BarLen)
    Download_Progress.grid(row=12, column=0)

    minecraft_versions = fetch_versions()
    minecraft_versions.insert(0, Config.Config["LastSelected"]) #using a bug in ttk to our advantage
    ListVariable = StringVar(MainWindow)
    Ver_List = ttk.OptionMenu(MainWindow, ListVariable, *minecraft_versions)
    Ver_List.configure(width=Config.ListLen) #only way i found of maintaining same width
    Ver_List.grid(row=10, column=0, sticky=W)
    
    log_info("Done!")
    MainWindow.mainloop()
