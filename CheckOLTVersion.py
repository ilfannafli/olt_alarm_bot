def CheckOLTVersion(input):
if input == "AN5516-04": 
            cmd = ["cd service",
                    "terminal length 0",
                    "cd .",
                    "cd maintenance",
                    "cd alarm",
                    "show alarm current"]

            for command in cmd:
                shell.send(command + "\n")
                #time.sleep(1)
                if command == "show alarm current":
                  shell.send(command + "\n")
                  time.sleep(3)   
                output = shell.recv(65535)                     

         #command list untuk OLT versi AN6000-2           
        if input == "AN6000-2": 
            cmd = ["config",
                    "terminal length 0",
                    "show alarm current"]
            for command in cmd:
                shell.send(command + "\n")
                #time.sleep(4)
                if command == "show alarm current":
                  shell.send(command + "\n")
                  time.sleep(4)
                output = shell.recv(65535)    