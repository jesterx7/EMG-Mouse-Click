class ThreadedClient:
"""
Launch the main part of the GUI and the worker thread. periodicCall and
endApplication could reside in the GUI part, but putting them here
means that you have all the thread controls in a single place.
"""
def _ _init_ _(self, master):
    """
    Start the GUI and the asynchronous threads. We are in the main
    (original) thread of the application, which will later be used by
    the GUI as well. We spawn a new thread for the worker (I/O).
    """
    self.master = master

    # Create the queue
    self.queue = Queue.Queue(  )

    # Set up the GUI part
    self.gui = GuiPart(master, self.queue, self.endApplication)

    # Set up the thread to do asynchronous I/O
    # More threads can also be created and used, if necessary
    self.running = 1
    self.thread1 = threading.Thread(target=self.workerThread1)
    self.thread1.start(  )

    # Start the periodic call in the GUI to check if the queue contains
    # anything
    self.periodicCall(  )

def periodicCall(self):
    """
    Check every 200 ms if there is something new in the queue.
    """
    self.gui.processIncoming(  )
    if not self.running:
        # This is the brutal stop of the system. You may want to do
        # some cleanup before actually shutting it down.
        import sys
        sys.exit(1)
    self.master.after(200, self.periodicCall)

def workerThread1(self):
    """
    This is where we handle the asynchronous I/O. For example, it may be
    a 'select(  )'. One important thing to remember is that the thread has
    to yield control pretty regularly, by select or otherwise.
    """
    while self.running:
        # To simulate asynchronous I/O, we create a random number at
        # random intervals. Replace the following two lines with the real
        # thing.
        time.sleep(rand.random(  ) * 1.5)
        msg = rand.random(  )
        self.queue.put(msg)

def endApplication(self):
    self.running = 0