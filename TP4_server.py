"""\
GLO-2000 Travail pratique 4 - Serveur
Noms et numéros étudiants:
-
-
-
"""

from email.message import EmailMessage
import hashlib
import hmac
import json
import os
import select
import smtplib
import socket
import sys

import glosocket
import gloutils


class Server:
    """Serveur mail @glo2000.ca."""

    def __init__(self) -> None:
        """
        Prépare le socket du serveur `_server_socket`
        et le met en mode écoute.

        Prépare les attributs suivants:
        - `_client_socs` une liste des sockets clients.
        - `_logged_users` un dictionnaire associant chaque
            socket client à un nom d'utilisateur.

        S'assure que les dossiers de données du serveur existent.
        """
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind(("localhost", gloutils.APP_PORT))
        self._server_socket.listen()
        self._client_socs = list()
        self._logged_users = dict()
        # ...

    def cleanup(self) -> None:
        """Ferme toutes les connexions résiduelles."""
        for client_soc in self._client_socs:
            client_soc.close()
        self._server_socket.close()
        self._client_socs.clear()
        self._logged_users.clear()

    def _accept_client(self) -> None:
        """Accepte un nouveau client."""
        client_socket = self._server_socket.accept()
        self._client_socs.append(client_socket)
        glosocket.send_msg(client_socket, "Bienvenue!")

    def _remove_client(self, client_soc: socket.socket) -> None:
        """Retire le client des structures de données et ferme sa connexion."""

    def _create_account(self, client_soc: socket.socket,
                        payload: gloutils.AuthPayload
                        ) -> gloutils.GloMessage:
        """
        Crée un compte à partir des données du payload.

        Si les identifiants sont valides, créee le dossier de l'utilisateur,
        associe le socket au nouvel l'utilisateur et retourne un succès,
        sinon retourne un message d'erreur.
        """
        # SAM : validation est fonctionnelle, reste à voir pour communication et tout
        username = payload['username']
        password = payload['password']

        account_valide = True
        username_check = username.replace("-", "")
        username_check = username_check.replace("_", "")
        username_check = username_check.replace(".", "")
        username_check = username_check.replace(" ", "")
        

        if not (username_check.isalnum()):
            account_valide = False
        
        pw_longueur = False
        if len(password) >= 10:
            pw_longueur = True

        pw_nombre = False
        pw_lower = False
        pw_upper = False
        for character in password:
            if character.isnumeric():
                pw_nombre = True
            elif character.islower():
                pw_lower = True
            elif character.isupper():
                pw_upper = True

        if not (pw_longueur and pw_lower and pw_nombre and pw_upper):
            account_valide = False

        if account_valide:
            """
            - crée dossier dans SERVER_DATA_DIR
            - Hache mdp sha3_512 et l'écrit dans PASSWORD_FILENAME
            - prévient client entête OK
            - associe socket avec username
            """
        else:
            entete_payload = gloutils.ErrorPayload(error_message="La création a échouée:\n - Le nom d'utilisateur est invalide.\n\
                                                                  - Le mot de passe n'est pas assez sûr.\n")
            message_envoye = gloutils.GloMessage(header=gloutils.Headers.ERROR, payload = entete_payload)
            glosocket.send_msg(self._server_socket, message_envoye)
            
        return gloutils.GloMessage()

    def _login(self, client_soc: socket.socket, payload: gloutils.AuthPayload
               ) -> gloutils.GloMessage:
        """
        Vérifie que les données fournies correspondent à un compte existant.

        Si les identifiants sont valides, associe le socket à l'utilisateur et
        retourne un succès, sinon retourne un message d'erreur.
        """
        return gloutils.GloMessage()

    def _logout(self, client_soc: socket.socket) -> None:
        """Déconnecte un utilisateur."""
        self._logged_users.pop(client_soc)
        client_soc.close()
        

    def _get_email_list(self, client_soc: socket.socket
                        ) -> gloutils.GloMessage:
        """
        Récupère la liste des courriels de l'utilisateur associé au socket.
        Les éléments de la liste sont construits à l'aide du gabarit
        SUBJECT_DISPLAY et sont ordonnés du plus récent au plus ancien.

        Une absence de courriel n'est pas une erreur, mais une liste vide.
        """
        return gloutils.GloMessage()

    def _get_email(self, client_soc: socket.socket,
                   payload: gloutils.EmailChoicePayload
                   ) -> gloutils.GloMessage:
        """
        Récupère le contenu de l'email dans le dossier de l'utilisateur associé
        au socket.
        """
        return gloutils.GloMessage()

    def _get_stats(self, client_soc: socket.socket) -> gloutils.GloMessage:
        """
        Récupère le nombre de courriels et la taille du dossier et des fichiers
        de l'utilisateur associé au socket.
        """
        return gloutils.GloMessage()

    def _send_email(self, payload: gloutils.EmailContentPayload
                    ) -> gloutils.GloMessage:
        """
        Détermine si l'envoi est interne ou externe et:
        - Si l'envoi est interne, écris le message tel quel dans le dossier
        du destinataire.
        - Si le destinataire n'existe pas, place le message dans le dossier
        SERVER_LOST_DIR et considère l'envoi comme un échec.
        - Si le destinataire est externe, transforme le message en
        EmailMessage et utilise le serveur SMTP pour le relayer.

        Retourne un messange indiquant le succès ou l'échec de l'opération.
        """
        return gloutils.GloMessage()

    def run(self):
        """Point d'entrée du serveur."""
        waiters = []
        while True:
            # Select readable sockets
            for waiter in waiters:
                # Handle sockets
                pass


def _main() -> int:
    server = Server()
    try:
        server.run()
    except KeyboardInterrupt:
        server.cleanup()
    return 0


if __name__ == '__main__':
    sys.exit(_main())
