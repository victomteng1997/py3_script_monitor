# python3 only
import subprocess
import os
import threading
from datetime import datetime



class py_monitor():

    def __init__(self, **kwargs):
        self.pid = int(os.getpid())
        self._check_compatibility()
        for key, value in kwargs.items():
            if "interval" == key:
                self.interval = value
            else:
                self.interval = 60
        self.records = []

    def _check_compatibility(self):
        try:
            ps = subprocess.check_output("which ps", shell=True)
            if ps.decode('utf-8') == True:
                raise Exception('Essential command "ps" not detected on system')
        except Exception as e:
            print("Error: ", e)
            return True
    
    def _get_time(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        return current_time

    
    def get_usage(self):
        # security check since shell is called
        if not self.pid or type(self.pid)!= int:
            return 
        ps = subprocess.check_output("ps aux | grep '%s'"%self.pid, shell=True)
        result = []
        output = ps.decode('utf-8')
        output = output.split("\n")
        result = []
        for line in output:
            try: 
                line_items = line.split()
                # doublecheck 
                if str(self.pid) == str(line_items[1]) and "grep" not in str(line):  
                    result.append(line)
                    cpu = line_items[2]
                    memory = line_items[3]
                    return {'%cpu':cpu, '%memory':memory}
            except Exception as e:
                # log the exception if needed
                print("Error: ", e)
                return None

    def record_usage(self):
        # record cpu and mem usage every interval second
        if not self.interval:
            print("No interval setted")
            return
        time = self._get_time()
        status = self.get_usage()
        
        # remove the following line to stop printing 
        print(time, status)
        
        
        self.records.append((time, status))
        self.t = threading.Timer(self.interval, self.record_usage)
        self.t.start()

    def stop_record_usage(self):
        self.t.cancel()
        
        




