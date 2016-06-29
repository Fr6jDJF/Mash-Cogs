def kill_red(bot):
    try:
        f = open("red.pid","r")
        bat_pid = f.readline()
        print("startRedLoop.bat: ", bat_pid)    
        print("active red: ", str(os.getpid()))

        try:
            if sys.platform == "linux" or sys.platform == "linux2":
                # linux
                """
                    start on runlevel [2345]
                    stop on runlevel [016]

                    respawn
                    chdir /home/username/Red-DiscordBot
                    setuid username
                    setgid username
                    exec python3.5 red.py --no-prompt
                                
                    post-start script
                    PID=`status app_name | egrep -oi '([0-9]+)$' | head -n1`
                        echo $PID > /home/username/Red-DiscordBot/red.pid
                    end script

                    post-stop script
                        rm -f /home/username/Red-DiscordBot/red.pid
                    end script  
                    ---------------------------------------------
                    #http://stackoverflow.com/questions/9972023/ubuntu-upstart-and-creating-a-pid-for-monitoring
                    #http://stackoverflow.com/questions/17856928/how-to-terminate-process-from-python-using-pid
                    #!upstart
                    description "Redis Server"

                    env USER=redis

                    start on startup
                    stop on shutdown

                    respawn

                    exec sudo -u $USER sh -c "/usr/local/bin/redis-server /etc/redis/redis.conf 2>&1 >> /var/log/redis/redis.log"

                    post-start script
                        PID=`status app_name | egrep -oi '([0-9]+)$' | head -n1`
                        echo $PID > /var/run/app_name.pid
                    end script

                    post-stop script
                    rm -f /var/run/app_name.pid
                    end script                         
                """
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
