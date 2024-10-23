import sqlite3

import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(   # g est un objet spécial unique pour chaque requête. Utilisé pour stocker des données auxquelles pls f° pvt accéder pdt la requête
            current_app.config['DATABASE'],   # current_app = autre objet spécial qui pointe vs l'appli flask qui gère la requête
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row    #sqlite3.row  indique à la connexion de renvoyer des lignes qui se comportent comme des dictionnaires, cela permet d'accéder aux colonnes par leyr nom

    return g.db


def close_db(e=None):   # close_db   vérifie si une connexion a été créé en vérifiant si g.db a été définie. Si la connexion existe, elle est fermée.
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)  # indique à Flask d'appeler cette fonction lors du nettoyage après avoir renvoyé la réponse
    app.cli.add_command(init_db_command)  # ajoute une nouvelle commande qui peut être appelée avec la flaskcommande



# fonctions python qui executeront ces commandes SQL au fichier db.py 
def init_db():
    db = get_db()   # get_db renvoie une connexion à la base de données, qui est utilisée pour exécuter les commandes lues dans le fichier.


@click.command('init-db')   # click.command()définit une commande de ligne de commande appelée init-db qui appelle la init_dbfonction et affiche un message de réussite à l'utilisateur.
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    

