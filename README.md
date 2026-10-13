# LES (laboratório de engenharia de software)

## Gestao de Pratica Diarias (web application for educational purposes)

### Used tool

 - Django
 - BootStrap
 - Html
 - Javascript

#### Creted by
 Nuno Pires, Daniel Stantchev, António Franco, José Ferreira, Ricardo Martins
 
![alt text](https://raw.githubusercontent.com/tonyamf/LES/master/LES.png)

## How to run

Requires Python 3.10 - 3.13. The commands below were run on Python 3.12.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate           # creates a fresh local db.sqlite3 (not stored in git)
python manage.py createsuperuser   # you choose the username and password
python manage.py runserver
```

Open http://127.0.0.1:8000/ and log in (every page requires login). The pages load Bootstrap,
jQuery and fonts from public CDNs, so the browser needs internet access for the styling to appear.

The project was originally written for Django 2.1.7 on Python 3.7 (`requirements-original.txt`).

### Tests

- `python manage.py test Activities Core Users Processes` runs, but those test files are empty stubs: 0 tests.
- `FuncionalTests/` holds Selenium browser tests. They need Firefox with geckodriver and an older
  Selenium (the code uses `find_element_by_*`, removed in Selenium 4.3); they are placeholders
  (one logs in as a hard-coded `admin`/`root` user). They have not been run successfully.

### Known limitations

- No sample data is included; the database starts empty.
- Deleting an object no longer shows the "deleted" message on Django 5 (the `delete()` override is not called by `DeleteView` any more).
- The root `models.py` is an unused `inspectdb` dump of an earlier database design.
