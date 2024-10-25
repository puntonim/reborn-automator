from datetime import date, datetime

import requests

from ..utils.log_utils import logger


class RebornApiClient:
    DEFAULT_HEADERS = headers = {"user-agent": "Dart/3.1 (dart:io)"}

    def __init__(self) -> None:
        self.session_id: str | None = None

    def login(self, username: str, password: str) -> None:
        """
        Example:
            $ curl -X POST https://reborn.shaggyowl.com/funzioniapp/v407/loginApp \
               -d "mail=rossi@gmail.com&pass=mypass&id_sede=47" \
               -H "user-agent: Dart/3.1 (dart:io)"

            {
                "status": 2,
                "messaggio": "Accesso effettuato con successo.",
                "parametri": {
                    "sessione": {
                        "isFacebook": 0,
                        "idFacebook": "",
                        "isGoogle": 0,
                        "idGoogle": "",
                        "idSede": "",
                        "idCliente": "206999",
                        "statoCliente": "",
                        "nomeCliente": "Paolo Rossi",
                        "cognomeCliente": "",
                        "mail": "rossi@gmail.com",
                        "pass": "",
                        "codice_sessione": "1729800784xxxxxxxxxx",
                        "path_img": "https://storage.shaggyowl.com/myapp/immagini/default/thumb-app-palestre.jpg",
                        "path_img_big": "https://storage.shaggyowl.com/myapp/immagini/default/thumb-app-palestre.jpg",
                        "sede": "{}",
                        "cliente": {},
                    },
                    "sedi_collegate": [
                        {
                            "nome": "Reborn",
                            "id_sede": "47",
                            "codice": "jkdGu3stmetropreborn",
                            "path_img": "image-picker-0e310cc0-cdc8-49cf-a514-83d17b522f77-1397-0000016136ebe886-1829569936.png",
                            "path_img_list": "https://storage.shaggyowl.com/myapp/immagini/img_rappr_sedi/152_152/image-picker-0e310cc0-cdc8-49cf-a514-83d17b522f77-1397-0000016136ebe886-1829569936.png",
                            "path_img_big": "https://storage.shaggyowl.com/myapp/immagini/img_rappr_sedi/image-picker-0e310cc0-cdc8-49cf-a514-83d17b522f77-1397-0000016136ebe886-1829569936.png",
                            "path_img_inner": "https://storage.shaggyowl.com/myapp/immagini/img_rappr_sedi/250_640/image-picker-0e310cc0-cdc8-49cf-a514-83d17b522f77-1397-0000016136ebe886-1829569936.png",
                            "active": 1,
                            "comune": "Torre Boldone",
                            "telefono": "3336286549",
                            "web": "http://www.youreborn.it/",
                            "mail": "info@youreborn.it",
                            "facebook": "https://www.facebook.com/yourebornofficial/",
                            "twitter": "",
                            "google": "",
                            "instagram": "https://www.instagram.com/yourebornofficial/?hl=it",
                            "testo": '<h6><span style="font-weight: normal;"><span style="font-size: 12px;"><i>Palestra funzionale presente sul territorio bergamasco dal 2011.<br></i></span><span style="font-size: 12px;"><i>La nostra forza sono l’elasticità e la professionalità. Lavoriamo con il cliente per essere sicuri di raggiungere ogni obiettivo, piccolo o grande che sia.</i></span></span></h6>',
                            "distance": "",
                            "indirizzo_completo": "Torre Boldone, Largo delle Industrie 9, 24020 Bergamo, LOMBARDIA",
                            "lat": "45.7096864",
                            "lon": "9.7141489",
                            "listaPagine": [
                                "home_utente_crossfit",
                                "palinsesto",
                                "wod",
                                "info_cliente",
                            ],
                            "id_stato_lavorazione": "3",
                            "lista_utenti": [],
                            "impostazioni_sede": {
                                "on_boarding": {
                                    "on_boarding_attivo": "2",
                                    "carta_di_credito_obbligatoria": "1",
                                    "on_boarding_sezioni": [
                                        {
                                            "key": "dati_utente",
                                            "campi_obbligatori": [
                                                "1",
                                                "2",
                                                "7",
                                                "8",
                                                "9",
                                                "12",
                                                "29",
                                            ],
                                            "tipologie": [],
                                        },
                                        {
                                            "key": "documenti",
                                            "campi_obbligatori": [],
                                            "tipologie": ["attestati_medici"],
                                        },
                                        {
                                            "key": "regolamenti",
                                            "campi_obbligatori": ["regolamento"],
                                            "tipologie": [],
                                        },
                                    ],
                                },
                                "sezioni_da_nascondere": [
                                    "servizi",
                                    "prenotazioni_campi",
                                    "shop",
                                    "multimedia",
                                    "disponibilita",
                                    "schede",
                                    "Multimedia",
                                ],
                                "impostazioni_abbonamenti": "",
                                "struttura_multimedia": [],
                                "filtri_staff_disponibilita": None,
                                "compenso_staff_ore_no_preno": "2",
                                "compenso_corsi_non_prenotabili": "2",
                                "mostra_priorita": "1",
                                "impostazioni_personalizzazione_app": {
                                    "primary_color_light": "#4d6fb2",
                                    "primary_color_dark": "#4d6fb2",
                                    "theme_mode": "both",
                                    "bottom_bar": [
                                        "home_utente_crossfit",
                                        "palinsesto",
                                        "wod",
                                        "info_cliente",
                                    ],
                                    "placeholder_pers_list": None,
                                    "bottom_bar_style": "Stile 1",
                                    "bottom_bar_fab": "servizi",
                                    "nascondere_numero_di_prenotati": "1",
                                    "permetti_modifica_livello": "1",
                                    "livelli": [
                                        {"id": "0", "nome": "Nessuno"},
                                        {"id": "1", "nome": "Base"},
                                        {"id": "2", "nome": "Base-Intermedio"},
                                        {"id": "3", "nome": "Intermedio"},
                                        {"id": "4", "nome": "Intermedio-Avanzato"},
                                        {"id": "5", "nome": "Avanzato"},
                                    ],
                                    "etichette": [
                                        {"id": "palinsesto", "nome": "Palinsesto"},
                                        {"id": "wod", "nome": "WOD"},
                                        {"id": "disponibilita", "nome": "Personal"},
                                        {"id": "schede", "nome": "Schede"},
                                        {"id": "abbonamenti", "nome": "Abbonamenti"},
                                        {"id": "sessioni", "nome": "Sessioni"},
                                        {"id": "wod_log", "nome": "WOD Log"},
                                        {"id": "corsi", "nome": "Corsi"},
                                        {"id": "prenotazioni", "nome": "Prenotazioni"},
                                        {"id": "prenotazioni_campi", "nome": "Campetti"},
                                        {"id": "info_cliente", "nome": "Le tue info"},
                                        {"id": "sede", "nome": "Centro"},
                                        {"id": "servizi", "nome": "Servizi"},
                                    ],
                                    "font": "Poppins",
                                },
                            },
                            "myapp": "2",
                            "indirizzo_android": "https://play.google.com/store/apps/details?id=com.shaggyowl.reborn&hl=it&gl=US",
                            "indirizzo_ios": "https://apps.apple.com/it/app/youreborn/id1398754364",
                        }
                    ],
                },
            }
        """
        logger.debug("Logging in...")
        url = "https://reborn.shaggyowl.com/funzioniapp/v407/loginApp"
        headers = {**self.DEFAULT_HEADERS}
        payload = {"mail": username, "pass": password}
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()

        self.session_id = (
            data.get("parametri", {}).get("sessione", {}).get("codice_sessione")
        )
        if self.session_id is None:
            raise AuthError(data)

    def get_palinsesto(self, sede_id: int = 47) -> dict:
        """
        Example:
            $ curl -X POST https://reborn.shaggyowl.com/funzioniapp/v407/palinsesti \
               -d 'id_sede=47&codice_sessione=172978952xxx&giorno=2024-10-25'
               -H "user-agent: Dart/3.1 (dart:io)"

            {
                "status": 2,
                "messaggio": "Tutto bene",
                "parametri": {
                    "lista_risultati": [
                        {
                            "id_palinsesti": "47",
                            "nome_palinsesto": "Lezioni Collettive",
                            "visibile": "2",
                            "principale": "2",
                            "tipo": "palinsesto",
                            "idclienti": "",
                            "id_cliente": "0",
                            "is_all_visible": "2",
                            "note": "",
                            "idclienti_array": [],
                            "tagsc": [],
                            "tagsc_value": "",
                            "tagsa": [],
                            "tagsa_value": "",
                            "giorni": [
                                {
                                    "orari_giorno": [
                                        {
                                            "id_orario_palinsesto": "748396",
                                            "is_online": "1",
                                            "no_greenpass": "1",
                                            "a_crediti": "1",
                                            "crediti": "0",
                                            "orario_inizio": "19:30",
                                            "orario_fine": "20:30",
                                            "via": "",
                                            "lat": "",
                                            "lon": "",
                                            "nota": "",
                                            "nome_corso": "Aerobic Capacity",
                                            "prenotabile_corso": "2",
                                            "iscrizioni": "2",
                                            "ingressi_corso": "1",
                                            "color_corso": "#339966",
                                            "prezzo": "0.00",
                                            "path_img_corso": "",
                                            "path_img_list_corso": "",
                                            "path_img_inner_corso": "",
                                            "path_img_big_corso": "",
                                            "path_img_small_corso": "",
                                            "staff": {
                                                "principali": [
                                                    {
                                                        "id_staff": "1649",
                                                        "nome": "Maria Luisa Bottini",
                                                        "color": "#a000ff",
                                                    }
                                                ],
                                                "secondari": [],
                                            },
                                            "nome_staff": "Maria Luisa Bottini",
                                            "nome_stanza": "",
                                            "nome_campo": "",
                                            "blocco_coda": 0,
                                            "multimedia": "1",
                                            "prenotazioni": {
                                                "numero_posti_disponibili": "9",
                                                "numero_utenti_coda": "0",
                                                "numero_utenti_attesa": "0",
                                                "numero_posti_occupati": "6",
                                                "id_disponibilita": "0",
                                                "nota": "",
                                                "utente_prenotato": "0",
                                                "frase": "Prenotazioni chiuse",
                                                "prenota_coda": "2",
                                            },
                                        },
                                        {
                                            "id_orario_palinsesto": "758744",
                                            "is_online": "1",
                                            "no_greenpass": "1",
                                            "a_crediti": "1",
                                            "crediti": "0",
                                            "orario_inizio": "20:00",
                                            "orario_fine": "21:00",
                                            "via": "",
                                            "lat": "",
                                            "lon": "",
                                            "nota": "",
                                            "nome_corso": "Calisthenics",
                                            "prenotabile_corso": "2",
                                            "iscrizioni": "2",
                                            "ingressi_corso": "1",
                                            "color_corso": "#ff0000",
                                            "prezzo": "0.00",
                                            "path_img_corso": "https://storage.shaggyowl.com/myapp/immagini/img_rappr_corsi/4-393962289.png",
                                            "path_img_list_corso": "https://storage.shaggyowl.com/myapp/immagini/img_rappr_corsi/152_152/4-393962289.png",
                                            "path_img_inner_corso": "https://storage.shaggyowl.com/myapp/immagini/img_rappr_corsi/250_640/4-393962289.png",
                                            "path_img_big_corso": "https://storage.shaggyowl.com/myapp/immagini/img_rappr_corsi/4-393962289.png",
                                            "path_img_small_corso": "https://storage.shaggyowl.com/myapp/immagini/img_rappr_corsi/0/small/4-393962289.png",
                                            "staff": {
                                                "principali": [
                                                    {
                                                        "id_staff": "1654",
                                                        "nome": "Matteo Artina",
                                                        "color": "#0084ff",
                                                    }
                                                ],
                                                "secondari": [],
                                            },
                                            "nome_staff": "Matteo Artina",
                                            "nome_stanza": "",
                                            "nome_campo": "",
                                            "blocco_coda": 0,
                                            "multimedia": "1",
                                            "prenotazioni": {
                                                "numero_posti_disponibili": "0",
                                                "numero_utenti_coda": "0",
                                                "numero_utenti_attesa": "0",
                                                "numero_posti_occupati": "16",
                                                "id_disponibilita": "0",
                                                "nota": "",
                                                "utente_prenotato": "10992911",
                                                "frase": "Sei prenotato per questo orario (16 p.)",
                                                "prenota_coda": "2",
                                            },
                                        },
                                    ],
                                    "nome_giorno": "Venerdì 25/10/2024",
                                    "giorno": "2024-10-25",
                                },
                                ...
                            ],
                        },
                        {
                            "id_palinsesti": "1931",
                            "nome_palinsesto": "Open Gym",
                            "visibile": "2",
                            "principale": "1",
                            "tipo": "palinsesto",
                            "idclienti": "",
                            "id_cliente": "0",
                            "is_all_visible": "2",
                            "note": "",
                            "idclienti_array": [],
                            "tagsc": [],
                            "tagsc_value": "",
                            "tagsa": [],
                            "tagsa_value": "",
                            "giorni": [
                                {
                                    "orari_giorno": [],
                                    "nome_giorno": "Giovedì 24/10/2024",
                                    "giorno": "2024-10-24",
                                },
                                {
                                    "orari_giorno": [],
                                    "nome_giorno": "Venerdì 25/10/2024",
                                    "giorno": "2024-10-25",
                                },
                                ...
                            ],
                        },
                    ]
                },
            }
        """
        logger.debug("Getting palinsesto...")
        url = "https://reborn.shaggyowl.com/funzioniapp/v407/palinsesti"
        headers = {**self.DEFAULT_HEADERS}
        payload = {"id_sede": sede_id, "codice_sessione": self.session_id}
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()

        return data

    def book_class(
        self, class_id: int, day: str | date | datetime, sede_id: int = 47
    ) -> dict:
        """
        Example:
            $ curl -X POST https://reborn.shaggyowl.com/funzioniapp/v407/prenotazione_new \
               -d 'id_sede=47&codice_sessione=1729789529xxx&id_orario_palinsesto=719536&data=2024-10-25'
               -H "user-agent: Dart/3.1 (dart:io)"

            {"status": 1, "messaggio": "Prenotazioni non aperte.", "parametri": {}}
        """
        logger.debug("Booking class...")
        if isinstance(day, str):
            day_str = day
        elif isinstance(day, date) or isinstance(day, datetime):
            day_str = day.strftime("%Y-%m-%d")
        else:
            raise NotADate(day)
        url = "https://reborn.shaggyowl.com/funzioniapp/v407/prenotazione_new"
        headers = {**self.DEFAULT_HEADERS}
        payload = {
            "id_sede": sede_id,
            "codice_sessione": self.session_id,
            "id_orario_palinsesto": class_id,
            "data": day_str,
        }
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        data = response.json()

        return data


class BaseRebornApiClientException(Exception):
    pass


class AuthError(BaseRebornApiClientException):
    def __init__(self, response_data: dict):
        self.response_data = response_data


class MissingDay(BaseRebornApiClientException):
    def __init__(self, data: dict):
        self.data = data


class NotADate(BaseRebornApiClientException):
    def __init__(self, value):
        self.value = value
