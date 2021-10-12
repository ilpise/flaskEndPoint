# Database


Per effetuare l'installazione del database

1. flask db init
2. flask db upgrade
3. flask db migrate

Per effettuare il seed del database
https://stackoverflow.com/questions/19334604/creating-seed-data-in-a-flask-migrate-or-alembic-migration
Ho modificato il file nella cartella migrations/versions ed ho aggiunto l'inserimento delle roles utilizzando op.bulk_insert

Per effettuare l'inserimento delle roles -> far girare le op.bulk_insert devi lanciare

1. flask db downgrade
2. flask db upgrade
3. flask db migrate

Nota - per le role non utliziamo l'indice di drupal in quanto le role in drupal sono a livello di gruppo

