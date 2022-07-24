from tkinter import *
from add_edit_anime import *
from tkinter import ttk
from stats_window import *


class AnilistView(Frame):
    """
    This class is a subclass of tkinter.Frame. The class houses the "main"
    app page, with the anilist and title. The bottom controls are separate
    and are located in the UI class.
    """
    def __init__(self, root_frame, controller, anime_list, anime_list_name):
        Frame.__init__(self,root_frame)
        self.pack(expand=TRUE,fill=BOTH)
        
        # Use the main UI class as a controller. This way the UI class' methods
        # are callable from here.
        self.__controller = controller

        # __al is the AnilistManager object that contains the actual anime list
        # data. 
        self.__al = anime_list
        self.__anilist_data = self.__al.anime_list_data
        self.__list_name = anime_list_name

        # Dict that stores all the widgets in the anime list
        # to make looping through them easy.
        self.__anime_widgets = {}
        
        # 'Top title' is the anilist's name (chosen by the user). It's
        # displayed at the top of the window
        self.__top_title = Label(self,
                                 text=self.__list_name,
                                 font=("Arial", 25),
                                 pady=20,
                                 padx=20)
        self.__top_title.pack(anchor="w")
        

        # Canvas component inside the root frame, apparently required for
        # scrollbars.
        self.__list_canvas = Canvas(self)
        self.__list_frame = Frame(self.__list_canvas,
                                  borderwidth=1,
                                  relief=RIDGE)
        
        # The scrollbar for the anime list
        self.__sb = Scrollbar(self,
                              orient=VERTICAL,
                              command=self.__list_canvas.yview)
        
        # Assign the scrollbar to the canvas
        self.__list_canvas.configure(yscrollcommand=self.__sb.set)
        
        # Bind the method 'on_configure' to the event 'Configure' (called
        # on resizing of the window etc.)
        self.__list_canvas.bind("<Configure>", self.on_configure)

        # Sets up the bar containing labels "Title", "Progress", etc.
        self.setup_top_bar()

        # Pack the scrollbar and canvas side by side
        self.__sb.pack(side=RIGHT,fill="y")
        self.__list_canvas.pack(side=LEFT,expand=TRUE,fill=BOTH)

        # Create a window inside the canvas and place '__list_frame' inside it
        self.__list_frame_id = \
            self.__list_canvas.create_window((0,0),window=self.__list_frame,
                                             anchor="nw")
        
        # Bind the list frame to on_configure
        self.__list_frame.bind("<Configure>", self.on_configure)
        
        self.populate_list_view()
    
    def setup_top_bar(self):
        """
        Sets up the top bar with the list descriptions. Widgets are stored
        inside 'description_bar_frame'. A 'stats' button is also displayed.
        It opens a window in which there is some statistics about the anime
        list.
        """
        description_bar_frame = Frame(self, borderwidth=2,relief=RIDGE)
        description_bar_frame.pack(fill="x")

        self.__anime_widgets["Top-bar"] = []
        title_label = Label(description_bar_frame, text="Title")
        title_label.grid(column=0,row=0)
        self.__anime_widgets["Top-bar"].append(title_label)

        # Columnconfigure sets the 'resizing weight' of the widget.
        # In this case the labels should be resized equally.
        # These options were fine tuned to match the anime list
        # displayed under this description bar.
        description_bar_frame.columnconfigure(0, weight=1)

        progress_label = Label(description_bar_frame,
                               text="Progress\n(watched/episodes)")
        progress_label.grid(column=2,row=0)
        self.__anime_widgets["Top-bar"].append(progress_label)
        description_bar_frame.columnconfigure(1, weight=1)

        rating_label = Label(description_bar_frame,
                             text="Rating\n(out of 100)")
        rating_label.grid(column=1,row=0)
        self.__anime_widgets["Top-bar"].append(rating_label)
        description_bar_frame.columnconfigure(2, weight=1)

        show_stats_button = Button(description_bar_frame,
                                   text="stats",
                                   command=self.open_stats_window)
        show_stats_button.grid(column=3,row=0,padx=(25,24))


    def on_configure(self,event):
        """
        This method is called whenever a change is made to the window.
        :param event: The event that happened, eg. window resize
        """
        # Set the scrollregions of the canvas to all of its contents.
        # This apparently has to happen continuously.
        # Set the width of '__list_frame' to the canvas width on resize.
        self.__list_canvas.configure(scrollregion=
                                     self.__list_canvas.bbox("all"))
        self.__list_canvas.itemconfig(self.__list_frame_id,
                                      width=self.__list_canvas.winfo_width())
        
        # Resize the anime list's widgets according to the window size
        # Sets the maximum widths inside their frames according to their
        # weights. 
        frame_width = self.__list_canvas.winfo_width()
        for i in self.__anime_widgets:
            for j in self.__anime_widgets[i]:
                j.configure(width=frame_width)
    
    def populate_list_view(self):
        """
        This function loads the anime list information onto UI elements.
        Each anime is displayed on one row. Visible items are anime name,
        number of episodes/the watch progress and the anime rating.

        Loops through all anime, creates labels for every piece of info
        of that anime (name, episodes, etc.) and places them inside their
        own frame 'anim_frame'.
        """
        current_row = 0

        # Show this text if there aren't any anime in the list.
        # This will be cleared when anime is added.
        if len(self.__anilist_data) == 0:
            add_new_anime_label = Label(self.__list_canvas, 
                                        text="It's empty here.\n" +
                                        "Add a new anime entry below!",
                                        font=('Arial', 11))
            add_new_anime_label.pack(fill=BOTH,expand=TRUE)
            add_new_anime_label.configure(anchor=CENTER)
            self.__list_frame.configure(borderwidth=0)
            return

        # Loops through all anime in the anime list datastructure and creates
        # a container frame for each anime. Creates widgets for the anime 
        # information and displays them in a list.
        for anime in sorted(self.__anilist_data):
            
            anim_frame = Frame(self.__list_frame)

            anim_frame.pack(fill="x",expand=TRUE,pady=10)
            
            # Get the anime information from the anime list
            title = self.__anilist_data.get(anime).title
            episodes = self.__anilist_data.get(anime).episodes
            rating = str(self.__anilist_data.get(anime).rating)
            watched = self.__anilist_data.get(anime).watched_episodes

            # These show up in the anime list in this order.
            anime_entry_properties = [title, rating, episodes]
            ap_list_len = len(anime_entry_properties)
            for i in range(0,ap_list_len):
                
                # Special treatment for episode label. Episodes are
                # shown as 'progress', aka as 5/25 episodes watched, for
                # example. The program expects the episode number to be
                # shown last in the anime list.
                if i == ap_list_len - 1:
                    property_text = f"{watched} / {anime_entry_properties[i]}"
                else:
                    # All the other labels are displayed as is
                    property_text = anime_entry_properties[i]
                
                anime_property = Label(anim_frame,
                                       text=property_text,
                                       font=("Arial", 12))

                anime_property.grid(row=current_row, column=i)
                
                # Adds the anime widgets to the widget dictionary
                # for easy looping.
                if anime in self.__anime_widgets:
                    self.__anime_widgets[anime].append(anime_property)
                else:
                    self.__anime_widgets[anime] = []
                    self.__anime_widgets[anime].append(anime_property)
                
                # Set the resizing weight of each anime entry property to 1
                anim_frame.columnconfigure(i,weight=1)

                # Set slightly smaller font for anime titles
                #if i == 0:
                #    anime_property.configure(font=('Arial', 11))
            

            # The '+1ep' button for each anime. The button's command is a 
            # lambda function with an argument 'a' which is set to the current
            # anime (or rather anime name). Doesn't work without the lambda
            # function attribute. The method 'watch_episode()' is called
            # when the button is pressed. The current anime name is passed as
            # a parameter.
            watch_episode_button = Button(anim_frame, text="+1ep",
                                          command=lambda a=anime:
                                          self.watch_episode(a))

            # Configure the button placement and resizing
            watch_episode_button.columnconfigure(ap_list_len + 1,weight=1)
            watch_episode_button.grid(row=current_row,
                                      column=ap_list_len + 1)

            # Add the edit button for each anime. Method 'edit_name()' is
            # called on button press, similar to +1ep button.
            edit_button = Button(anim_frame, text="...",
                                 command=lambda a=anime:
                                 self.edit_anime(a))

            edit_button.columnconfigure(ap_list_len + 2, weight=1)
            edit_button.grid(row=current_row,
                             column=ap_list_len + 2,
                             padx=(2,10))

            # Adds a nice row separator between each anime entry
            row_separator = ttk.Separator(self.__list_frame,orient=HORIZONTAL)
            row_separator.pack(fill="x")

            current_row += 1

    def watch_episode(self, anime_name):
        """
        Adds one episode to the watched episodes of *anime_name*. Only does it if
        not all episodes are watched yet. This function expects that the
        'progress' widget is the last widget in the corresponding anime's
        anime widgets dict/list. Calls the ani object's method watch_episode(),
        not to be confused with the name of this function.
        :param anime_name: str, the name of the anime
        """

        anime = self.__anilist_data[anime_name]
        anime.watch_episode()
        progress_label = self.__anime_widgets[anime_name][-1]
        progress_label.configure(text= f"{anime.watched_episodes} / " + 
                                       f"{anime.episodes}")
    
    def open_stats_window(self):
        """
        Opens the anime stats window.
        """
        StatsWindow(self.__controller.mainw, self.__al)

    def edit_anime(self, anime):
        """
        Is called when the edit anime button is pressed. Calls
        the controller's 'edit_anime()' method.
        :param anime: str, the name of the anime that gets edited
        """
        self.__controller.edit_anime(anime)
        