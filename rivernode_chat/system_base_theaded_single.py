import sys
import os
import time

from threading import Thread

class SystemBaseThreadedSingle(object):

    def __init__(self):
        super(SystemBaseThreadedSingle, self).__init__()
        self.thread = Thread(target=self.run)
        self.thread.daemon = True
        self.thread_is_running = False

    #Implement this
    def prepare(self):
        pass

    #Implement this
    def work(self):
        pass

    def start(self):
        if self.thread_is_running:
            raise RuntimeError('System alreaddy running')
        self.thread.start()
        while not self.thread_is_running: #await preparation complete
            time.sleep(0.01)


    def stop(self, timeout=0):
        if not self.thread_is_running:
            raise RuntimeError('System not running')
        self.thread_is_running = False
        self.thread.join(timeout)

    def await_stop(self, timeout=None):
        self.thread.join(timeout)

    def run(self):
        try:
            self.prepare()    
            self.thread_is_running = True        
        except Exception as exception:
            print('Exception on prepare')
            print(exception)
            sys.stdout.flush()
            self.thread_is_running = False
            
            #TODO exeption to main tread and inform ebs controller that start failed?

        while(self.thread_is_running):
            try:
                self.work()          
            except Exception as exception:
                print(exception)
                print('Exception on work')
                
                sys.stdout.flush()
                pass
                #TODO exeption to main tread and inform ebs controller that work failed
        print('run thread done ')
        sys.stdout.flush()