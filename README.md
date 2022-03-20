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

---

## Catch

Be sure before submission that all files comments have author tags replaced with student IDs or are removed

Sorry for the code, it is a small mess. Most code is in the [screen.py](/screen.py) file. But I blame that on Tkinter, not myself or any of us.
