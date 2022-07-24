from anime import *

class Anilist:
    """
    Anilist handles the file reading and writing. It
    also stores the anime list.
    """
    def __init__(self, filename):

        # Structure: {'Anime name': Anime object}
        # Houses the raw anime list data.
        self.anime_list_data = {}

        self.__filename = filename
        self.list_name = ""

    def load_anilist(self):
        """
        Assuming file *filename* exists, we can open the file and read it.
        """
        
        file = open(self.__filename, "r")
        
        line_num = 1
        for line in file:
            # Removes newline from the end of the line
            line = line.strip()

            if line_num > 1:
                contents = line.split(";")

                title = contents[0]
                episodes = contents[1]
                watched_episodes = contents[2]
                rating = contents[3]
                
                # Creates an Anime object with the information read from each
                # line as parameters. That anime object is saved to the
                # anime list data structure.
                self.anime_list_data[title] = Anime(title,
                                                   episodes,
                                                   watched_episodes,
                                                   rating)
            else:
                # Gets the anime list's name from the file's first line 
                self.list_name = line

            line_num += 1

        file.close()


    def save_anilist(self):
        """
        This function writes whatever is in the *anime_list* data structure
        to anilist.csv one anime per row as per the file format.
        """

        lines_to_write = []
        lines_to_write.append(self.list_name+"\n")
        for anime in self.anime_list_data:
            cur_anime = self.anime_list_data[anime]
            line = f"{cur_anime.title};{cur_anime.episodes};"+ \
                   f"{cur_anime.watched_episodes};{cur_anime.rating}\n"

            lines_to_write.append(line)

        file = open(self.__filename, "w")
        file.writelines(lines_to_write)
        file.close()
    
    def get_stats(self):
        """
        Returns the current anilist stats:
        number of anime, episodes watched and average rating in this order.
        """

        ald = self.anime_list_data

        total_anime = len(ald)
        total_episodes = 0
        
        rating_sum = 0

        for anime in ald:
            total_episodes += int(ald[anime].watched_episodes)
            
            # Shows rated 0 won't count to 'avg_rating' as 0 is the
            # default rating
            anime_rating = int(ald[anime].rating)
            if anime_rating != 0:
                rating_sum += anime_rating
        if total_anime != 0:
            avg_rating = rating_sum / total_anime

            # Returns the total number of anime, episodes and the average rating
            # rounded to a one decimal accuracy.
            return str(total_anime), str(total_episodes), f"{avg_rating:.1f}"
        
        return str(0), str(0), str(0)
    
    def add_or_edit_anime(self, title, episodes, watched, rating):
        """
        Adds an anime to the list and saves the list.
        """
        self.anime_list_data[title] = Anime(title, episodes, watched, rating)
        self.save_anilist()

    def delete_anime(self, title):
        """
        Deletes an anime from the list.
        """
        del self.anime_list_data[title]
        self.save_anilist()



