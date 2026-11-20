from app import App
from console_io import ConsoleIO
from tietokanta import Tietokanta
from tulostus import Tulostus
def main():
    """konstruoidaan tarvittavat luokat ja annetaan eteenpäin, lopuksi app käyntiin"""
    console_io = ConsoleIO()
    tietokanta = Tietokanta()
    tulostus = Tulostus(console_io)
    app = App(console_io, tietokanta, tulostus)
    app.run()

if __name__ == "__main__":
    main()
