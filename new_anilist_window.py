from tkinter import *
from tkinter import messagebox

FILENAME = "anilist.csv"


class NewAnilistWindow(Toplevel):
    """
    When initialized, this class displays a toplevel window in which the user
    can create a new anime list (when one doesn't exist).
    """
    def __init__(self, root_window, controller):

        # Set the root window to the main window
        self.__root = root_window

        # Set the controller to the AnilistApp object
        self.__controller = controller
        
        # Call the toplevel constructor
        Toplevel.__init__(self, self.__root)
        self.__root.withdraw()

        self.__created_new = False

        self.bind("<Destroy>", self.window_destroyed)

        # Setup window contents (labels etc) and assign commands to buttons
        self.title("New anilist")
        self.geometry("250x125")
        self.minsize(width=250,height=125)
        self.__list_name = Entry(self,width=50)
        self.__name_label = Label(self, text="Anilist name")

        self.__name_label.pack()
        self.__list_name.pack(padx=20)

        self.__control_frame = Frame(self)
        self.__control_frame.pack(pady=10)
        self.__cancel_button = Button(self.__control_frame, text="Cancel",
                                      command=self.destroy)

        self.__new_list_button = Button(self.__control_frame, text="Create",
                                        command=self.new_anilist)

        
        self.__new_list_button.pack(side=LEFT,padx=5)
        self.__cancel_button.pack(side=RIGHT,padx=5)

    
    def window_destroyed(self, event):
        """
        This function is called when this window (or actually any widget) is
        destroyed either by pressing the exit button or the cancel button
        (linked to self.destroy()). The function checks if a new anilist was 
        created before destruction. If the anilist is created, the flag
        *cancel_pressed* in the main will remain false, thus showing the anime
        list view after showing the main window again.
        :param event: The widget event
        """
        if event.widget == self:
            if not self.__created_new:
                self.__controller.cancel_pressed = True
            self.__root.deiconify()

    
    def new_anilist(self):
        """
        Creates the file "anilist.csv" with the name of the anime list. Shows 
        a message box after the successful file creation. The anime list name
        can't contain 
        """
        anilist_name = self.__list_name.get()

        # Checks name for semicolons
        if ";" in anilist_name:
                messagebox.showwarning(
                    message="Name must not contain semicolons.")
                return

        # Creates the anilist.csv file and saves the list name to it
        file = open(FILENAME, "w")
        file.write(anilist_name)
        file.close()
        messagebox.showinfo(message=f"Anime list {anilist_name}"+
                                    "created successfully.")
        self.__created_new = True
        self.destroy()

