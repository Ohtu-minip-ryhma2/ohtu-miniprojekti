from app import App
from console_io import ConsoleIO

def main():
    """konstruoidaan tarvittavat luokat ja annetaan eteenpäin, lopuksi app käyntiin"""
    console_io = ConsoleIO()
    app = App(console_io)
    app.run()

# tämä on ainakin testejä varten, mutta ilmeisesti täyttää myös muita pythinin standardeja vaatiuksia.
if __name__ == "__main__":
    main()
