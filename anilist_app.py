from tkinter import *
from anime import *
from new_anilist_window import *
from anilistview import *
from anilist import *
from add_edit_anime import *

# The anime list filename is constant
FILENAME = "anilist.csv"

class AnilistApp:
    """
    The App class contains the program's main user interface and functionality.
    This class also acts as a controller for the other classes/toplevel
    windows used in this program.
    """

    def __init__(self):
        # Init the main window. Declared public for visibility reasons.
        self.mainw = Tk()
        
        self.__anime_list = None

        # Everything will be displayed inside the 'main frame'
        # so that destroying all widgets is easy when needed.
        # The frame is initialized later on.
        self.__main_frame = None

        # The name of the anime list
        self.__anilist_name = ""

        # Flag attribute keeping track on if a cancel button
        # has been pressed inside other windows.
        self.cancel_pressed = False

        # Start by looking for the anilist file
        self.look_for_file()
        
        # Bind the method 'on_close' to the main window destroy event
        self.mainw.bind("<Destroy>", self.on_close)

        # Run the main window loop
        self.mainw.mainloop()

    def on_close(self, event):
        """
        Saves the anime list on exit.
        """
        if event.widget == self.mainw:
            # Only save if an anime list exists (aka isn't None)
            if not isinstance(self.__anime_list, type(None)):
                self.__anime_list.save_anilist()

    def look_for_file(self):
        """
        Looks for the file anilist.csv. The anime list will be loaded
        if found. A splash screen telling the user that no list was found
        the file doesn't exist.
        """
        try:
            file = open(FILENAME, "r")
            file.close()
            self.load_anime_list()
        except OSError:
            self.no_list_found()

    def load_anime_list(self):
        """
        Loads the anime list and displays it.
        """

        # All widgets inside the window will reside in this 'root' frame.
        self.__main_frame = Frame(self.mainw,borderwidth=1,relief=RIDGE)
        self.__main_frame.pack(expand=1,fill=BOTH)

        # Initializes the anime list (manager) object. 
        self.__anime_list = Anilist(FILENAME)

        # Load the anilist from file
        self.__anime_list.load_anilist()

        # Get the anilist name from the anime list object
        self.__anilist_name = self.__anime_list.list_name

        # Set the window width, title and minimum dimensions
        self.mainw.geometry("970x660")
        self.mainw.title(f"Anilist - {self.__anilist_name}")
        self.mainw.minsize(width=970,height=660)

        anilist_frame = AnilistView(self.__main_frame, self,
                                    self.__anime_list,
                                    self.__anilist_name)
        
        # Shows the bottom controls (Add anime, quit)
        self.show_bottom_bar()

    def no_list_found(self):
        """
        Displays a splash screen telling the user that an anime list
        was not found. The user can then create and name one themselves.
        """
        self.__main_frame = Frame(self.mainw)
        self.__main_frame.pack()

        no_list_found = Label(self.__main_frame,
                                text="No anilist found.\nCreate new anilist?")

        new_button = Button(self.__main_frame, text="Create new",
                            command=self.new_anilist)

        self.mainw.title("Anilist")

        self.mainw.geometry("220x100")
        self.mainw.minsize(width=220,height=100)
        no_list_found.pack(pady=10)
        new_button.pack()
    
    def new_anilist(self):
        """
        Creates and displays the 'add new anilist' window.
        """
        # Create and show the "add new anime" window
        nalw = NewAnilistWindow(self.mainw, self)

        # Pause the main window loop until the new anilist window
        # is closed.
        self.mainw.wait_window(nalw)
        
        # Check if action was cancelled
        if self.cancel_pressed:
            self.cancel_pressed = False
            return
        
        # If the cancel button wasn't pressed, proceed to load and show the
        # anime list.
        self.__main_frame.destroy()
        self.load_anime_list()
    
    def show_bottom_bar(self):
        """
        Shows the bottom controls (ie. 'Add anime' and 'Quit')
        """
        bottom_controls = Frame(self.__main_frame,borderwidth=1,relief=RAISED)
        bottom_controls.pack(fill="x")

        quit_button = Button(bottom_controls,
                                    text="Quit",
                                    command=self.mainw.destroy)

        add_button = Button(bottom_controls,
                                   text="Add anime",
                                   command=self.add_new_anime)
        
        quit_button.pack(side=RIGHT,pady=10,padx=(2,10))
        add_button.pack(side=RIGHT,pady=10)

        
    def add_new_anime(self):
        """
        Opens the add new anime/edit anime window with 'add mode' enabled.
        Calls the method 'refresh_main_ui' which will check if cancel
        was pressed in the popup window.
        """
        new_anime_window = AddEditAnime(self.mainw,
                                           self,
                                           self.__anime_list,
                                           add_mode=True)
        # Disables interaction with the main window while
        # new anime window is open
        new_anime_window.grab_set()

        # Pause the main window until the current window is closed
        self.mainw.wait_window(new_anime_window)

        self.refresh_main_ui()

    def edit_anime(self, anime_title):
        """
        Opens the add new anime/edit anime window with 'add mode' disabled.
        (=> opens it in edit mode)
        Calls the method 'refresh_main_ui' which will check if cancel
        was pressed in the popup window.
        """
        
        ea_window = AddEditAnime(self.mainw,
                                 self,
                                 self.__anime_list,
                                 add_mode=False,
                                 edited_anime=anime_title)

        ea_window.grab_set()
        self.mainw.wait_window(ea_window)

        self.refresh_main_ui()

    def refresh_main_ui(self):
        """
        Handles the cleanup and reloading after the previous window was closed.
        """

        # Don't do anything further if the previous action was cancelled
        if self.cancel_pressed:
            self.cancel_pressed = False
            return
        
        # Destroy the contents of the main window and reload the
        # anime list.
        self.__main_frame.destroy()
        self.load_anime_list()

    def del_anime(self, anime_title):
        """
        Called from other classes when an anime needs to be deleted.
        :param anime_title: str, the title of the anime that gets deleted
        """
        self.__anime_list.delete_anime(anime_title)
        