from datetime import date, datetime
from enum import StrEnum
from functools import lru_cache

from ..clients.reborn_api_client import RebornApiClient
from ..conf import settings
from ..utils import datetime_utils
from ..utils.log_utils import logger


class ClassNameEnum(StrEnum):
    CALI = "Calisthenics"
    POWER = "Powerlifting"


class BookClassDomain:
    def __init__(self, sede_id: int = 47):
        self.client = RebornApiClient()
        self.sede_id = sede_id

    @lru_cache
    def _login(self):
        self.client.login(
            settings.REBORN_CREDS_USERNAME, settings.REBORN_CREDS_PASSWORD
        )

    def get_next_calisthenics_class(self):
        return self._get_next_class(class_name=ClassNameEnum.CALI)

    def get_next_powerlifting_class(self):
        return self._get_next_class(class_name=ClassNameEnum.POWER)

    def _get_next_class(
        self, class_name: str | ClassNameEnum
    ) -> tuple[int, dict, date]:
        """
        Returns:
            (
                758744,
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
                            {"id_staff": "1654", "nome": "Matteo Artina", "color": "#0084ff"}
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
                date(2024, 10, 25),
            )
        """
        logger.debug(f"Getting next {class_name} class...")
        self._login()
        palinsesto = self.client.get_palinsesto(self.sede_id)

        # Traverse all results.
        for risultato in palinsesto.get("parametri", {}).get("lista_risultati", []):
            risultato: dict
            if risultato.get("nome_palinsesto") != "Lezioni Collettive":
                continue

            # Traverse all days.
            for giorno in risultato.get("giorni", []):
                # Make sure the day is tomorrow or later.
                day_str: str | None = giorno.get("giorno")  # Eg. "2024-10-25".
                if not day_str:
                    raise MissingDay(giorno)
                day_date: date = datetime.strptime(day_str, "%Y-%m-%d").date()
                if (day_date - datetime_utils.now().date()).days <= 0:
                    # It's today, yesterday or earlier.
                    continue

                # Traverse all classes.
                for klass in giorno.get("orari_giorno"):
                    klass: dict
                    # Checking the class name.
                    if klass.get("nome_corso") != class_name:
                        continue
                    # Make sure there is a class id.
                    klass_id = klass.get("id_orario_palinsesto")
                    if klass_id is None:
                        raise MissingIdOrarioPalinsesto(klass)
                    return klass_id, klass, day_date
        raise NoClassFoundInPalinsesto(class_name)

    def book_next_calisthenics_class(self):
        return self._book_next_class(ClassNameEnum.CALI)

    def book_next_powerlifting_class(self):
        return self._book_next_class(ClassNameEnum.POWER)

    def _book_next_class(self, class_name: str | ClassNameEnum) -> tuple[dict, date]:
        """
        Returns:
            {"status": 1, "messaggio": "Prenotazioni non aperte.", "parametri":{}}
        """
        logger.debug(f"Booking next {class_name} class...")
        self._login()
        try:
            class_id, _, day_date = self._get_next_class(class_name)
        except NoClassFoundInPalinsesto:
            raise
        day_date: date
        data = self.client.book_class(
            class_id=class_id, day=day_date, sede_id=self.sede_id
        )
        if data.get("status") != 2:
            raise FailedBooking(data, class_name, class_id, day_date)
        return data, day_date


class BaseBookClassDomainException(Exception):
    pass


class MissingDay(BaseBookClassDomainException):
    def __init__(self, data: dict):
        self.data = data


class MissingIdOrarioPalinsesto(BaseBookClassDomainException):
    def __init__(self, data: dict):
        self.data = data


class FailedBooking(BaseBookClassDomainException):
    def __init__(
        self,
        response: dict,
        class_name: str | ClassNameEnum,
        class_id: int,
        day_date: date,
    ):
        self.response = response
        self.class_name = class_name
        self.class_id = class_id
        self.day_date = day_date


class NoClassFoundInPalinsesto(BaseBookClassDomainException):
    def __init__(self, class_name: str):
        self.class_name = class_name
