# Aqui tuve el mismo problema, Al ejecutar coverage, me decia que me faltaba un 1% por que no probaba la llamada a la funcion main de la ultima linea de codigo
# Asi que para evitar que saliera asi, enseguida de if __name__ == "__main__": agregue # pragma: no cover para que no lo considere
# coverage al ejecutarse. De esa forma si sale el 100%

import unittest
from unittest.mock import patch, mock_open, MagicMock
import ej2


class TestSong(unittest.TestCase):
    def setUp(self):
        self.title = "Papercut"
        self.author = "Linkin Park"
        self.album = "Hybrid theory"
        self.year = 2001
        self.obj = ej2.Song(self.title, self.author, self.album, self.year)

    def test_init(self):
        self.assertEqual(self.title, self.obj.title)
        self.assertEqual(self.author, self.obj.author)
        self.assertEqual(self.album, self.obj.album)
        self.assertEqual(self.year, self.obj.year)

    @patch("builtins.print")
    def test_display(self, mock):
        l = []
        l.append(f"Title: {self.title}")
        l.append(f"Author: {self.author}")
        l.append(f"Album: {self.album}")
        l.append(f"Year: {self.year}")
        self.obj.display()
        for msg in l:
            mock.assert_any_call(msg)


class TestSongStore(unittest.TestCase):
    def setUp(self):
        self.store = ej2.SongStore()

    @patch("builtins.print")
    def test_add_song(self, mock_print):
        song = ej2.Song("Title1", "Author1", "Album1", 2020)
        self.store.add_song(song)
        self.assertEqual(len(self.store.songs), 1)
        self.assertEqual(self.store.songs[0], song)
        mock_print.assert_called_with("Song 'Title1' added to the store.")

    @patch("builtins.print")
    def test_display_songs_empty(self, mock_print):
        self.store.display_songs()
        mock_print.assert_called_with("No songs in the store.")

    @patch("builtins.print")
    def test_display_songs_with_data(self, mock_print):
        song1 = MagicMock()
        song2 = MagicMock()
        self.store.songs = [song1, song2]
        self.store.display_songs()
        mock_print.assert_any_call("Songs available in the store:")
        self.assertEqual(song1.display.call_count, 1)
        self.assertEqual(song2.display.call_count, 1)

    @patch("builtins.print")
    def test_search_song_not_found(self, mock_print):
        self.store.songs = []
        self.store.search_song("Hello")
        mock_print.assert_called_with("No song found with title 'Hello'.")

    @patch("builtins.print")
    def test_search_song_found(self, mock_print):
        song1 = MagicMock()
        song1.title = "Hello"
        song2 = MagicMock()
        song2.title = "hello"
        self.store.songs = [song1, song2]
        self.store.search_song("HELLO")
        mock_print.assert_any_call("Found 2 song(s) with title 'HELLO':")
        self.assertEqual(song1.display.call_count, 1)
        self.assertEqual(song2.display.call_count, 1)


class TestMain(unittest.TestCase):
    @patch("builtins.input", side_effect=["1", "4"])
    @patch("ej2.SongStore.display_songs")
    @patch("builtins.print")
    def test_main_display_songs(self, mock_print, mock_display, mock_input):
        ej2.main()
        mock_display.assert_called_once()

    @patch("builtins.input", side_effect=["2", "Hello", "4"])
    @patch("ej2.SongStore.search_song")
    @patch("builtins.print")
    def test_main_search_song(self, mock_print, mock_search, mock_input):
        ej2.main()
        mock_search.assert_called_once_with("Hello")

    @patch("builtins.input", side_effect=["3", "T1", "A1", "AL1", "2020", "4"])
    @patch("ej2.SongStore.add_song")
    @patch("builtins.print")
    def test_main_add_song(self, mock_print, mock_add, mock_input):
        ej2.main()
        self.assertEqual(mock_add.call_count, 1)
        args = mock_add.call_args[0]
        song = args[0]
        self.assertEqual(song.title, "T1")
        self.assertEqual(song.author, "A1")
        self.assertEqual(song.album, "AL1")
        self.assertEqual(song.year, 2020)

    @patch("builtins.input", side_effect=["5", "4"])
    @patch("builtins.print")
    def test_main_invalid_option(self, mock_print, mock_input):
        ej2.main()
        mock_print.assert_any_call("Invalid choice. Please try again.")

    @patch("builtins.input", side_effect=["4"])
    @patch("builtins.print")
    def test_main_exit(self, mock_print, mock_input):
        ej2.main()
        mock_print.assert_any_call("Exiting...")
