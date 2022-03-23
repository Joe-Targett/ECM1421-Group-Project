# ECM1421-Group-Project

Group Project for Exeter Course ECM1421 Python GUI Pilot Project

Required Packages:

- tkinter
- pyodbc

This package will work both Windows and Unix-like systems.

---

## Trusted Login

To run, run the [main.py](/main.py) file. This does require SQL Server login and not trusted login though.

To do trusted login replace the `main` function in [main.py](/main.py) with:

```python
def main():
    screen = Screen()
    screen.set_database(Database())
    screen.list_customer_screen()
    screen.mainloop()
```

When in trusted login mode, be sure not to return to the login screen.
