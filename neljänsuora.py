from tkinter import *
from functools import partial

# TIE-02100 Johdatus Ohjelmointiin
# Graafisen käyttöliittymän suunnittelu ja toteutus: Skaalautuva

# Neljänsuora peli.

# Käyttöohjeet: neljänsuora.py tiedoston suorittaminen avaa ensiksi setup
# ikkunan. Setup ikkunaan on tarkoitus syöttää haluttu rivien ja sarakkeiden
# määrä, jonka perusteella pelin pelikenttä luodaan. Virallinen pelikentän koko
# on 6x7. Rivien ja sarakkeiden minimi ja maksimi määrät on rajattu, jotta peli
# säilyttää pelattavuutensa. Kun olet syöttänyt arvot paina nappia "Start Game"
# ja peli käynnistyy, jos arvot ovat hyväksytty. Neljänsuora ikkuna avautuu ja
# setup ikkuna katoaa.
# Neljänsuora ikkunan selitys:
# Neljänsuora ikkunan ylimmältä riviltä löydät Labelin,
# joka kertoo käynnissä olevan pelin tilanteen tai lopputuloksen. Ylärivin
# oikeasta reunasta löytyy New Game ja Exit Game napit, joilla aloitetaan uusi
# peli(New Game) tai poistutaan pelistä(Exit Game). Toiselta riviltä löytyvät
# "Place Mark Here" napit. Nämä napit toimivat niin, että nappia painaessa
# vuorossa olevan pelaajan pelimerkki putoaa alimmalle vapaalle riville, joka
# on napin kanssa samassa sarakkeessa. Rivit ja sarakkeet ovat numeroitu
# ikkunan selventämiseksi. Pelikenttä löytyy nappien ja sarake Labelien
# alapuolelta (rivi Labelien oikealta puolelta). Pistetilanne ilmestyy
# ensimmäisen pelin jälkeen vasempaan yläreunaan
# SÄÄNNÖT:
# Pelissä edetään vuorotellen pudottaen merkkejä halutun sarakkeen alimmalle
# vapaalle riville. Pelin tavoitteena on saada neljä merkkiä 'suoraan' eli
# saada neljä omaa merkkiä joko vaakasuorasti, pystysuorasti tai vinosti
# peräkkäin. Pelin voittaa tähän tavoitteeseen ensimmäiseksi päässyt pelaaja.
# Jos kaikki sarakkeet täyttyvät ilman, että yksikään pelaaja pääsee
# tavoitteeseen, on peli päättynyt tasapeliin.


class Neljansuora:
    def __init__(self):
        self.__engine = Tk()
        self.__engine.title('Neljänsuora')

        self.__turn = 0
        self.__won = False
        self.__draw_counter = 0
        self.__wins = {'BLUE': 0, 'RED': 0}

        self.__empty = PhotoImage(file="empty.gif")
        self.__blue = PhotoImage(file="blue.gif")
        self.__red = PhotoImage(file="red.gif")

        # DICTS TO KEEP TRACK OF GAME
        self.__field = {}
        self.__filled_spots = {}
        for i in range(columns):
            self.__filled_spots[i] = rows

        # LABELS
        self.__turn_label = Label(self.__engine)
        self.__turn_label.configure(text="Blue's turn", bg='white', font=30)
        self.__turn_label.grid(row=0, column=columns//2, columnspan=3,
                               sticky=W)
        self.__wins_label = Label(self.__engine)
        self.__wins_label.grid(row=0, column=0, sticky=W)

        for i in range(rows):
            Label(self.__engine, text='|ROW ' + str(i + 1) + "|").\
                grid(row=3+i, column=0)
        for i in range(columns):
            Label(self.__engine, text='|COLUMN ' + str(i + 1) + '|').\
                grid(row=2, column=1+i)

        self.__playground = []
        p = 0  # Used only in for loop
        for i in range(rows):
            for b in range(columns):
                new_label = Label(self.__engine)
                self.__playground.append(new_label)
                self.__playground[p].configure(image=self.__empty, bg='green')
                self.__playground[p].grid(row=3+i, column=1 + b)
                p += 1

        # BUTTONS
        self.__buttons = []
        for i in range(columns):
            new_button = Button(self.__engine)
            self.__buttons.append(new_button)
            self.__buttons[i].configure(text="Place Mark Here",
                                        command=partial(self.place_mark, i),
                                        bg='white')
            self.__buttons[i].grid(row=1, column=1+i)

        Button(self.__engine, text='New Game', command=self.new_game,
               bg='green').grid(row=0, column=columns-1, sticky=E)

        Button(self.__engine, text='Exit Game', command=self.exit, bg='red').\
            grid(row=0, column=columns)

    def start(self):
        """
        Starts the game window
        :return: None
        """
        self.__engine.mainloop()

    def new_game(self):
        """"
        Used to reset current game and start a new one
        :return: None
        """
        for label in self.__playground:
            label.configure(image=self.__empty)
        self.__turn = 0
        self.__won = False
        self.__draw_counter = 0
        self.__turn_label.configure(text="Blue's turn", bg='white')
        self.__filled_spots = {}
        for i in range(columns):
            self.__filled_spots[i] = rows
        self.__field = {}
        self.change_buttons_state(ACTIVE)

    def exit(self):
        """
        Used to close the game window
        :return: None
        """
        self.__engine.destroy()

    def place_mark(self, mark):
        """
        Places marker on first open spot (from bottom) on the wanted column
        and also calls methods to check draw and win status.
        :param mark: tells which column marker is wanted to be placed at
        :return: None
        """
        if self.__turn % 2 == 0:
            player = 'BLUE'
        else:
            player = 'RED'

        column = mark + 1
        row = self.__filled_spots[mark]

        if player == 'BLUE':
            self.__playground[(row * columns - 1) - (columns - column)]. \
                configure(image=self.__blue)
        else:
            self.__playground[(row * columns - 1) - (columns - column)]. \
                configure(image=self.__red)

        self.__field[row, mark] = player
        self.check_win(player)

        if not self.__won:
            self.__filled_spots[mark] = row - 1
            if self.__filled_spots[mark] == 0:
                self.__buttons[mark].configure(state=DISABLED, bg='grey')
                self.__draw_counter += 1
                self.check_draw()

            if not self.__won:
                self.__turn += 1
                if player == 'BLUE':
                    self.__turn_label.configure(text="Red's turn.")
                else:
                    self.__turn_label.configure(text="Blue's turn.")

    def check_win(self, player):
        """
        Checks if player has won the game. If player has won the game
        calls method has_won
        :param player: Player whose win status is being checked
        :return: None
        """
        # CHECK HORIZONTAL
        for (x, y) in self.__field:
            if self.__field[x, y] == player:
                if (x-1, y) in self.__field and self.__field[x-1, y] == player:
                    if (x-2, y) in self.__field and self.__field[x-2, y]\
                            == player:
                        if (x-3, y) in self.__field and self.__field[x-3, y]\
                                == player:
                            self.has_won(player)

        # CHECK VERTICAL
        for (x, y) in self.__field:
            if self.__field[x, y] == player:
                if (x, y-1) in self.__field and self.__field[x, y-1] == player:
                    if (x, y-2) in self.__field and self.__field[x, y-2]\
                            == player:
                        if (x, y-3) in self.__field and self.__field[x, y-3]\
                                == player:
                            self.has_won(player)

        # CHECK DIAGONAL
        for (x, y) in self.__field:
            if self.__field[x, y] == player:
                if (x-1, y-1) in self.__field and self.__field[x-1, y-1]\
                        == player:
                    if (x-2, y-2) in self.__field and self.__field[x-2, y-2]\
                            == player:
                        if (x-3, y-3) in self.__field and\
                                self.__field[x-3, y - 3] == player:
                            self.has_won(player)

        for (x, y) in self.__field:
            if self.__field[x, y] == player:
                if (x-1, y+1) in self.__field and self.__field[x-1, y+1]\
                        == player:
                    if (x-2, y+2) in self.__field and self.__field[x-2, y+2]\
                            == player:
                        if (x-3, y+3) in self.__field and \
                                self.__field[x-3, y + 3] == player:
                            self.has_won(player)

    def check_draw(self):
        """
        Checks if game has ended in draw (all spots have been filled without
        filling win criters). If game has ended in draw lets the players know
        game has ended in draw.
        :return: None
        """
        if self.__draw_counter == columns:
            self.__won = True
            self.__turn_label.configure(text='DRAW!', bg="yellow")

    def change_buttons_state(self, state):
        """
        Easily change state of all buttons to ACTIVE or DISABLED depending on
        situation
        :param state: Wanted state for all buttons
        :return: None
        """
        for button in self.__buttons:
            button.configure(state=state)
            if state == ACTIVE:
                button.configure(bg='white')
            else:
                button.configure(bg='grey')

    def has_won(self, player):
        """
        Let players know who has won and also how many games each player
        has won.
        :param player: Player who has won.
        :return: None
        """
        self.__won = True
        self.__wins[player] += 1
        self.__wins_label.configure(text='BLUE: ' + str(self.__wins['BLUE']) +
                                         ' RED: ' + str(self.__wins['RED']))

        self.__turn_label.configure(text=player + ' has won the game!',
                                    bg=player)
        self.change_buttons_state(DISABLED)


def start_ui(setup_tk, rows_entry, columns_entry, error_label):
    """
    Checks values entered to setup Tkinter window. If values are correct
    setup window is closed and values are set to global so they can be used
    in the actual game.
    :param setup_tk: Tkinter window for setup
    :param rows_entry: Entry where rows are entered
    :param columns_entry: Entry where columns are entered
    :param error_label: Used to let user know if values are incorrect
    :return: None
    """
    try:
        rows1 = int(rows_entry.get())
        columns1 = int(columns_entry.get())
        if 5 <= rows1 <= 12 and 6 <= columns1 <= 13:
            setup_tk.destroy()
            global rows, columns
            rows = rows1
            columns = columns1
        else:
            raise ValueError

    except ValueError:
        rows_entry.delete(0, END)
        columns_entry.delete(0, END)
        error_label.configure(text='Check inputs')


def setup():
    """
    Makes setup window where user can enter values he wants the game to use.
    :return: None
    """
    setup_tk = Tk()
    setup_tk.title('Setup')

    Label(setup_tk, text='Rows (5-12): ').grid(row=0, column=0)
    Label(setup_tk, text='Columns (6-13): ').grid(row=1, column=0)

    rows_entry = Entry(setup_tk)
    rows_entry.grid(row=0, column=1)

    columns_entry = Entry(setup_tk)
    columns_entry.grid(row=1, column=1)

    error_label = Label(setup_tk)
    error_label.grid(row=0, column=2)

    Button(setup_tk, text='Start Game', command=partial(
        start_ui, setup_tk, rows_entry, columns_entry, error_label)).\
        grid(row=1, column=2)

    setup_tk.mainloop()


def main():
    setup()
    ui = Neljansuora()
    ui.start()


main()
