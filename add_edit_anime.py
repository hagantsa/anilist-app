from tkinter import *
from tkinter import messagebox
from anime import *

class AddEditAnime(Toplevel):
    """
    This class when initialized opens up a toplevel window in which
    the user can either add a new anime or edit an existing one.
    """
    def __init__(self,
                 root_window,
                 controller,
                 anime_list,
                 add_mode=True,
                 edited_anime=None):
        # The root window (main window)
        self.__root = root_window

        # The controller class, aka AnilistApp
        self.__controller = controller
        
        # The anime list object containing the anime list data structure
        self.__anime_list = anime_list

        # The raw anime list data structure
        self.__anilist_data = self.__anime_list.anime_list_data

        # Bool, decides if the window should be opened in 'add' mode or
        # in 'edit' mode. Add mode is enabled if set to true.
        self.__add_mode = add_mode

        # The title of the anime being edited
        self.__edited_anime = edited_anime

        # Initialize the toplevel window
        Toplevel.__init__(self, self.__root)

        # Set some window options
        self.geometry("350x200")
        self.resizable(False,False)

        # Method 'window_destroyed' gets called on a 'Destroy' event.
        # aka when a widget or window gets destroyed.
        self.bind("<Destroy>", self.window_destroyed)
        
        # Window contents
        self.__input_frame = Frame(self)
        self.__input_frame.pack(padx=10)

        self.__anime_title_label = Label(self.__input_frame,
                                         text="Title:")

        self.__anime_title_entry = Entry(self.__input_frame)

        self.__anime_episodes_label = Label(self.__input_frame,
                                            text="Episodes:")

        self.__anime_episodes_entry = Entry(self.__input_frame)

        self.__anime_rating_label = Label(self.__input_frame,
                                          text="Rating:")

        self.__anime_rating_entry = Entry(self.__input_frame)
        
        self.__episodes_watched_label = Label(self.__input_frame, 
                                              text="Episodes watched:")

        self.__episodes_watched_entry = Entry(self.__input_frame)

        self.__control_frame = Frame(self)

        self.__done_button = Button(self.__control_frame, text="Done",
                                    command=self.check_inputs)

        self.__cancel_button = Button(self.__control_frame, text="Cancel",
                                      command=self.on_cancel)

        self.__delete_anime_button = Button(self.__input_frame,
                                            text="Delete anime",
                                            command=self.on_delete)

        self.__anime_title_label.grid(row=0,column=0,sticky="w")
        self.__anime_title_entry.grid(row=1,column=0)
        self.__anime_episodes_label.grid(row=2,column=0,sticky="w")
        self.__anime_episodes_entry.grid(row=3,column=0)
        self.__anime_rating_label.grid(row=4,column=0,sticky="w")
        self.__anime_rating_entry.grid(row=5,column=0)
        self.__episodes_watched_label.grid(row=6,column=0,sticky="w")
        self.__episodes_watched_entry.grid(row=7,column=0)

        self.__control_frame.pack(pady=5,padx=10,anchor="e")
        self.__cancel_button.pack(side=RIGHT)
        self.__done_button.pack(side=RIGHT)
        
        # Flag that is flipped to true, if the cancel button is pressed
        self.__cancelled = False

        # Set some window options based on if add or edit mode is in use
        if self.__add_mode:
            self.title("Add Anime")
        else:
            # Show the 'delete anime' button if in edit mode
            self.__delete_anime_button.grid(row=8,column=0,pady=(10,0))
            self.title("Edit Anime")
            self.geometry("350x240")

            # Load the anime info into the text fields
            self.load_info_on_edit()

    def on_cancel(self):
        """
        Called when the cancel button is pressed. Flips the bool
        '__cancelled'
        """
        self.__cancelled = True
        self.destroy()


    def window_destroyed(self, event):
        """
        Called whenever a window (or actually other widgets) gets destroyed.
        Checks if the Destroy event was this window's event.
        If the action was cancelled, the controller's flag 'cancel_pressed'
        will be set to true.
        :param event: the event that happened
        """
        if event.widget == self:
            if self.__cancelled:
                self.__controller.cancel_pressed = True
            self.__root.deiconify()

    def on_delete(self):
        """
        Is called when the delete button is clicked.
        """
        # Asks the controller to delete the current anime, aka the anime
        # that is being edited. Lastly this window is destroyed.
        self.__controller.del_anime(self.__edited_anime)
        self.destroy()

    def check_inputs(self):
        """
        Function that checks the entry field inputs for validity. An error
        message is displayed if the entries aren't valid.
        """

        # Get the entry values
        title = self.__anime_title_entry.get()
        episodes = self.__anime_episodes_entry.get()
        rating = self.__anime_rating_entry.get()
        watched = self.__episodes_watched_entry.get()

        # Check for semicolons
        if ";" in title:
            messagebox.showinfo(message="Title must not contain semicolons.")
            return

        # Check if the title of new anime already exists in the list
        if self.__add_mode:    
            if title in self.__anilist_data:
                messagebox.showinfo(message=f"Anime {title} " +
                                             "already exists in the list.")
                return

        # Check if the rest of the fields contain valid types. If the rating 
        # field is empty, default the value to 0.
        try:
            episodes_int = int(episodes)
            watched_int = int(watched)
            if rating.strip() != "":
                rating_int = int(rating)
            else:
                rating_int = 0
        except ValueError:
            messagebox.showinfo(message="Inputs other than name" + 
                                " must be positive integers (or zero).\n" +
                                "Rating can be left blank, in which case the" +
                                " default rating is 0.")
            return
        
        # Check if watched episodes is less or equal to the number of episodes
        if watched_int > episodes_int:
            messagebox.showinfo(message="Watched episodes cannot be greater " +
                                        "than total number of episodes!")
            return

        # Check if the numerical fields have good values
        for i in [episodes_int,rating_int,watched_int]:
            if i < 0:
                messagebox.showinfo(message="Inputs other than name" + 
                                " must be positive integers (or zero).\n"+
                                "The anime rating must be an integer in "+ 
                                "the range 0-100.")
                return
        
        if self.__add_mode:
            self.add_anime(title, episodes, watched, rating_int)
            return
        
        self.edit_anime(title, episodes, watched, rating_int)

    def add_anime(self, title, episodes, watched, rating):
        """
        Adds a new anime to the anime list and shows a message box
        on successfull addition.
        """
        self.__anime_list.add_or_edit_anime(title, episodes, watched, rating)

        messagebox.showinfo(message=f"{title} added to the list.")
        
        # Destroy the window
        self.destroy()

    def edit_anime(self, new_title, new_episodes, new_watched, new_rating):
        """
        Edits an existing anime on the list. Basically just adds a new anime
        to the list and deletes the anime with the old title if needed.
        """
        self.__anime_list.add_or_edit_anime(new_title,
                                            new_episodes,
                                            new_watched,
                                            new_rating)
        
        # If the title is edited, remove the anime list entry with the
        # old title.
        if self.__edited_anime != new_title:
            self.__anime_list.delete_anime(self.__edited_anime)

        messagebox.showinfo(message=f"Anime entry {new_title} updated.")
        self.destroy()

    def load_info_on_edit(self):
        """
        Loads the current anime's info into the edit window's entry boxes.
        """
        anime_title = self.__edited_anime

        anime_episodes = self.__anilist_data[anime_title].episodes
        anime_watched = self.__anilist_data[anime_title].watched_episodes
        anime_rating = self.__anilist_data[anime_title].rating
        
        self.__anime_title_entry.insert(0, anime_title)
        self.__anime_episodes_entry.insert(0, anime_episodes)
        self.__episodes_watched_entry.insert(0, anime_watched)
        self.__anime_rating_entry.insert(0, anime_rating)
