from ui.main_window import MainWindow
import database

if __name__ == "__main__":
    database.create_table()

    app = MainWindow()
    app.mainloop()
