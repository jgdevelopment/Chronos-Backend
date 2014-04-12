export DATABASE_URL=postgres://jason:dum04sci@localhost:5432/historical

heroku run python manage.py syncdb

heroku run python manage.py blsImports Oil.csv oil
