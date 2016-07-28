def kill_red(bot):
    try:
        f = open("red.pid","r")
        bat_pid = f.readline()
        print("startRedLoop.bat: ", bat_pid)    
        print("active red: ", str(os.getpid()))

        try:
            if sys.platform == "linux" or sys.platform == "linux2":
                # linux
                bot.logout()
                os.popen('kill -SIGTERM '+str(bat_pid))
            elif sys.platform == "darwin":
                # OS X
                bot.logout()
            elif sys.platform == "win32":
                # Windows... 
                bot.logout()
                # Kill the proces using pywin32 and pid
                import win32api
                PROCESS_TERMINATE = 1
                handle = win32api.OpenProcess(PROCESS_TERMINATE, False, int(bat_pid))
                win32api.TerminateProcess(handle, -1)
                win32api.CloseHandle(handle)
                exit()
        except Exception as e:
            print("Kill PID error")
            print (e)
            return False
    except Exception as e:
        print("Read PID error")
        print (e)
        #bot.logout()
        return False

# Available Tasks
class StartThread():
    def __init__ (self, instructor="unknown", thread=None):
        self.instructor = instructor
        self.taskname = "StartThread"
        self.thread = thread

class StopThread():
    def __init__ (self, instructor="unknown", thread=None):
        self.instructor = instructor
        self.taskname = "StopThread"
        self.thread = thread        
        
class StartTray():
    def __init__ (self, instructor="unknown",):
        self.instructor = instructor    
        self.taskname = "StartTray"
        
class StopTray():
    def __init__ (self, instructor="unknown",):
        self.instructor = instructor    
        self.taskname = "StopTray"
        
class ReloadTray():
    def __init__ (self, instructor="unknown",):
        self.instructor = instructor
        self.taskname = "ReloadTray"
        
class QuitRed():
    def __init__ (self, instructor="unknown",):    
        self.instructor = instructor
        self.taskname = "QuitRed"        

class UpdateMenu():
    def __init__ (self, instructor="unknown", data=None):
        self.instructor = instructor
        self.taskname = "UpdateMenu"
        self.data = data
                
class HideConsole():
    def __init__ (self, instructor="unknown"):
        self.instructor = instructor
        self.taskname = "HideConsole"
        
class ShowConsole():
    def __init__ (self, instructor="unknown"):
        self.instructor = instructor
        self.taskname = "ShowConsole"
        
class ToggleConsole():
    def __init__ (self, instructor="unknown"):
        self.instructor = instructor
        self.taskname = "ToggleConsole"        

class BalloonInfo():
    def __init__ (self, instructor="unknown", title=None, msg=None):
        self.instructor = instructor
        self.taskname = "BalloonInfo"
        self.title = title
        self.msg = msg

class ToolTip():
    def __init__ (self, instructor="unknown", tooltip=None):
        self.instructor = instructor
        self.taskname = "ToolTip"
        self.tooltip = tooltip
        
class ChangeIcon():
    def __init__ (self, instructor="unknown", icon=ICON_FILE):
        self.instructor = instructor
        self.taskname = "ChangeIcon"
        self.icon = icon
        
class InstallCog():
    def __init__ (self, instructor="unknown", cog=None):
        self.instructor = instructor
        self.taskname = "InstallCog"
        self.cog = cog
        
class LoadCog():
    def __init__ (self, instructor="unknown", cog=None):
        self.instructor = instructor
        self.taskname = "LoadCog"
        self.cog = cog
        
class UnloadCog():
    def __init__ (self, instructor="unknown", cog=None):
        self.instructor = instructor
        self.taskname = "UnloadCog"
        self.cog = cog
        
class ReloadCog():
    def __init__ (self, instructor="unknown", cog=None):
        self.instructor = instructor
        self.taskname = "ReloadCog"
        self.cog = cog
        
class OpenBrowser():
    def __init__ (self, instructor="unknown", url=None):
        self.instructor = instructor
        self.taskname = "OpenBrowser"
        self.url = url

# Development sub menu
class prep_dev_menu():
    def __init__(self, state):
        global trayQueue
        self.state = state
        self.sub_menu = ()

    def add_tasks(self, cog=None, op=None, url=None, title="Error building menu ", msg="Check cog_operations()", icon=ICON_FILE2):
        instr = "devmenu"
        if op == "rl":# Reload
            q = trayQueue.put(ReloadCog(instr, cog))
        elif op == "ul":# Unload
            q = trayQueue.put(UnloadCog(instr, cog))
        elif op == "ld":# Load
            q = trayQueue.put(LoadCog(instr, cog))
        elif op == "pop":# Pop baloon text
            q = trayQueue.put(BalloonInfo(instr, title, msg))
        elif op == "owb":# Web browser
            q = trayQueue.put(OpenBrowser(instr, url))
        elif op == "inst":# Install
            q = trayQueue.put(InstallCog(instr, og))
        elif op == "swico":# Switch icon
            q = trayQueue.put(ChangeIcon(instr, icon))
        elif op == "fresh":# Refresh menu
            menu_options = ()
            menu_options += ("\o/ Useless shitty menu", None, lambda event: print("1"), "GRAYED"), 
            menu_options += ("Checked item", None,  lambda event: print("2"), "CHECKED"), 
            menu_options += ("RADIO_CHECKED item", None,  lambda event: print("3"), "RADIO_CHECKED"), 
            menu_options += ("RADIO_UNCHECKED item", None,  lambda event: print("4"), "RADIO_UNCHECKED"), 
            menu_options += ("TEXT item", None,  lambda event: print("5"), "TEXT"),
            prep_menu = [None, None, None, menu_options]
            q = trayQueue.put(UpdateMenu(instr, prep_menu))
        else:
            q = trayQueue.put(BalloonInfo(instr, title, msg))
        return q

    def list_options(self, data=None):
        list_options = ()
        list_options += ("some", None,  lambda event: print(data), None),
        return list_options
        
    def create_sub(self):          
        self.sub_menu = ()
        self.sub_menu += ("Clear command line", None, lambda event: cls_cmd(), self.state),
        self.sub_menu += ("Switch Icon", None, lambda event: self.add_tasks(op="swico", icon=ICON_FILE2), self.state),
        self.sub_menu += ("Refresh tray menu", None, lambda event: self.add_tasks(op="fresh"), self.state),     
        #self.sub_menu += ("Monkey", None, self.list_options("Banana"), None),        
        return self.sub_menu
