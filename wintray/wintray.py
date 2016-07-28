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
