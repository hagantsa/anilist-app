from tkinter import *

class StatsWindow(Toplevel):
    """
    When initializes, opens a toplevel window containing some statistics
    about the current anime list. Will display 0 on all stats, if there
    is no anime added. No other functionality than a 'close' button.
    """
    def __init__(self, root_window, anilist):
        self.__al = anilist
        self.__root = root_window
        Toplevel.__init__(self, self.__root)

        self.setup_window()
    
    def setup_window(self):
        """
        Set up the window widgets. 
        """
        container_frame = Frame(self)
        container_frame.pack()

        Label(container_frame, text="Total anime:").grid(row=0, column=0,
                                                         sticky="w",
                                                         padx=20,
                                                         pady=20)

        Label(container_frame, text="Total episodes watched:").grid(row=1, 
                                                                    column=0,
                                                                    sticky="w",
                                                                    padx=20,
                                                                    pady=20)

        Label(container_frame, text="Average rating:").grid(row=2,
                                                            column=0,
                                                            sticky="w",
                                                            padx=20,
                                                            pady=20)
        # Get the anime list stats
        num_anime, episodes, avg_rating = self.__al.get_stats()

        Label(container_frame, text=num_anime).grid(row=0,
                                                    column=1,
                                                    sticky="e",
                                                    padx=20,
                                                    pady=20)

        Label(container_frame, text=episodes).grid(row=1,
                                                    column=1,
                                                    sticky="e",
                                                    padx=20,
                                                    pady=20)

        Label(container_frame, text=avg_rating).grid(row=2,
                                                    column=1,
                                                    sticky="e",
                                                    padx=20,
                                                    pady=20)
        self.geometry("310x270")
        self.resizable(False, False)
        
        close_button = Button(self,text="Close",command=self.destroy)
        close_button.pack(pady=10)

