Anilist 5000 - A program for tracking your anime watch history.
(also works for any other TV show or movie). If anime is not something
you are familiar with, it is basically Japanese animated TV shows and
movies.

The following files are required to use the program:
main.py (this file)
anilist_app.py (the 'main class' (even though it's separate from main.py),
                contains the user interface stuff and acts as a controller
                of some sort for the other classes. The controller is
                responsible for displaying new windows etc.)
anime.py (simple class for anime objects)
animelist.py (wrapper for the underlying anime list data structure, also
              handles most of the IO stuff)
anilistview.py (subclass of *tkinter.Frame()*, houses the anime list and its
                widgets)
newanilistwindow.py (subclass of *tkinter.Toplevel()*, a window for creating
                     a new anime list)
add_edit_anime.py (subclass of *tkinter.Toplevel()*, a window for adding or
                   editing an anime entry. The mode depends on a constructor
                   parameter)
stats_window.py (a window displaying some statistics regarding the anime list)

(technically optional):
anilist.csv (contains the saved anime list data)

The idea of this program is to provide the user a tool to track their anime 
watch history (or technically any other TV show/movie).You can add new anime to
the list along with the information of the anime. When you have watched an
episode of the anime, you can track your progress with this app. Each anime
has a "+1ep" button in the list, with which you can increment the episode
counter. Each anime also has a '...' button, with which you can edit the
anime information and/or title and set a new rating for example.

On top of the list there is also a 'stats' button, which will open up
a window containing some statistics based on your anime list.

When adding new anime or editing an existing entry, the app should warn about
the following incorrect inputs:
- the anime title can contain anything, except for semicolons (due to the csv'
file structure)
- the anime episodes, watched episodes and rating must be positive integers
(or zero)
- the rating can be left blank and will default to 0

The anime list is displayed in alphabetical order.

Anilist 5000 saves your anime list into a file "anilist.csv" in the project
directory. If the file doesn't exist, the app will ask you to create a new
anime list with a name of your choice, eg. "John's anime list". If the file 
"anilist.csv" already exists, then the app will load that anime list. The list 
file should always be valid if the user creates their list using this app
(although the format is easy to use manually too). This app always expects
a valid file, so manually creating one can break the app.

The app has a dynamically adjusting user interface, where the widgets are
resized along with the window.

You can start using the app by loading the sample anilist.csv and later
try out a fresh start by deleting the sample anilist.
