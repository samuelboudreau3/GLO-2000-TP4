"""\
GLO-2000 Travail pratique 4 - Client
Noms et numéros étudiants:
-
-
-
"""

import argparse
import getpass
import json
import socket
import sys

import glosocket
import gloutils
import string

class Client:
    """Client pour le serveur mail @glo2000.ca."""

    def __init__(self, destination: str) -> None:
        """
        Prépare et connecte le socket du client `_socket`.

        Prépare un attribut `_username` pour stocker le nom d'utilisateur
        courant. Laissé vide quand l'utilisateur n'est pas connecté.
        """
        self._client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client_socket.connect((destination, gloutils.APP_PORT))
        self._username = None 

    def _register(self) -> None:
        """
        Demande un nom d'utilisateur et un mot de passe et les transmet au
        serveur avec l'entête `AUTH_REGISTER`.

        Si la création du compte s'est effectuée avec succès, l'attribut
        `_username` est mis à jour, sinon l'erreur est affichée.
        """
        username = input("Entrez un nom d'utilisateur: ")
        password = getpass.getpass("Entrez un mot de passe: ")
        payload = gloutils.AuthPayload(username=username, password=password)
        auth_message = gloutils.GloMessage(header=gloutils.Headers.AUTH_REGISTER, payload=payload)
        glosocket.send_msg(self._client_socket, json.dumps(auth_message))
        response = glosocket.recv_msg(self._client_socket)
        if json.loads(response)['header'] == gloutils.Headers.OK:
            self._username = username
        if json.loads(response)['header'] == gloutils.Headers.ERROR:
            pass

    def _login(self) -> None:
        """
        Demande un nom d'utilisateur et un mot de passe et les transmet au
        serveur avec l'entête `AUTH_LOGIN`.

        Si la connexion est effectuée avec succès, l'attribut `_username`
        est mis à jour, sinon l'erreur est affichée.
        """
        username = input("Entrez votre nom d'utilisateur: ")
        password = getpass.getpass("Entrez votre mot de passe: ")
        payload = gloutils.AuthPayload(username=username, password=password)
        auth_message = gloutils.GloMessage(header=gloutils.Headers.AUTH_LOGIN, payload=payload)
        glosocket.send_msg(self._client_socket, json.dumps(auth_message))
        response = glosocket.recv_msg(self._client_socket)
        if json.loads(response)['header'] == gloutils.Headers.OK:
            self._username = username

    def _quit(self) -> None:
        """
        Préviens le serveur de la déconnexion avec l'entête `BYE` et ferme le
        socket du client.
        """
        bye_message = gloutils.GloMessage(header=gloutils.Headers.BYE)
        glosocket.send_msg(self._client_socket, json.dumps(bye_message))
        self._client_socket.close()

    def _read_email(self) -> None:
        """
        Demande au serveur la liste de ses courriels avec l'entête
        `INBOX_READING_REQUEST`.

        Affiche la liste des courriels puis transmet le choix de l'utilisateur
        avec l'entête `INBOX_READING_CHOICE`.

        Affiche le courriel à l'aide du gabarit `EMAIL_DISPLAY`.

        S'il n'y a pas de courriel à lire, l'utilisateur est averti avant de
        retourner au menu principal.
        """
        entete = gloutils.GloMessage(header=gloutils.Headers.INBOX_READING_REQUEST)
        glosocket.send_msg(self._client_socket, json.dumps(entete))
        inbox = glosocket.recv_msg(self._client_socket)
        print(inbox) #??? est-ce que c'est tout simplement une liste qu'on reçoit






    def _send_email(self) -> None:
        """
        Demande à l'utilisateur respectivement:
        - l'adresse email du destinataire,
        - le sujet du message,
        - le corps du message.

        La saisie du corps se termine par un point seul sur une ligne.

        Transmet ces informations avec l'entête `EMAIL_SENDING`.
        """
        dest = input("Entrez l'adresse email du destinataire")
        sujet = input("Entrez le sujet du message")
        print("Entrez le contenu du courriel, terminez la saisie avec un '.' seul sur une ligne:")
        corps = ""
        bool_corps = True
        while bool_corps == True:
            input_corps = input()
            if input_corps == '.':
                bool_corps = False
            else:
                corps += input_corps + '\n'
        entete_payload = gloutils.EmailContentPayload(sender=self._username, 
                                                      destination=dest, 
                                                      subject=sujet, 
                                                      date=gloutils.get_current_utc_time(),
                                                      content=corps)
        entete = gloutils.GloMessage(header=gloutils.Headers.EMAIL_SENDING, payload=entete_payload)
        glosocket.send_msg(self._client_socket, json.dumps(entete))

    def _check_stats(self) -> None:
        """
        Demande les statistiques au serveur avec l'entête `STATS_REQUEST`.

        Affiche les statistiques à l'aide du gabarit `STATS_DISPLAY`.
        """

    def _logout(self) -> None:
        """
        Préviens le serveur avec l'entête `AUTH_LOGOUT`.

        Met à jour l'attribut `_username`.
        """
        logout_message = gloutils.GloMessage(header=gloutils.Headers.AUTH_LOGOUT)
        glosocket.send_msg(self._client_socket, json.dumps(logout_message))
        self._username = None

    def run(self) -> None:
        """Point d'entrée du client."""
        should_quit = False

        while not should_quit:
            if not self._username:
                # Authentication menu
                print(gloutils.CLIENT_AUTH_CHOICE)
                options = {
                    1: self._register,
                    2: self._login,
                    3: self._quit,
                }
                selection = int(input(f'Entrez votre choix [1-{len(options)}]: '))
                options[selection]()
                if selection == 3:
                    should_quit = True
                pass
            else:
                # Main menu
                print(gloutils.CLIENT_USE_CHOICE)
                options = {
                    1: self._read_email,
                    2: self._send_email,
                    3: self._check_stats,
                    4: self._logout
                }
                selection = int(input(f'Entrez votre choix [1-{len(options)}]: '))
                options[selection]()
                pass


def _main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--destination", action="store",
                        dest="dest", required=True,
                        help="Adresse IP/URL du serveur.")
    args = parser.parse_args(sys.argv[1:])
    client = Client(args.dest)
    client.run()
    return 0


if __name__ == '__main__':
    sys.exit(_main())
