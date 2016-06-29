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
