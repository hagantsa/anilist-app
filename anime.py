class Anime:
    """
    This class represents an Anime. It's attributes include the anime
    name, num of episodes, num of watched episodes and rating. Note: attributes
    are marked as public to easily available. The anime rating defaults at 0. The
    rating scale is 0-100.
    """
    def __init__(self, title, episodes, watched_episodes, rating="0"):
        
        self.title = title
        self.episodes = episodes
        self.watched_episodes = watched_episodes
        self.rating = rating

    def watch_episode(self):
        """
        Increases 'watched_episodes' by one. The value is saved as a string
        for easy operation with tkinter widgets. Only increments the value
        if watched_episodes != episodes.
        """
        we = int(self.watched_episodes)
        if we + 1 <= int(self.episodes):
            we += 1
            self.watched_episodes = str(we)


    