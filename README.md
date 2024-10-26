**Reborn Automator**
====================

Automate the booking of classes at Reborn gym in Torre Boldone.\
This project is based on a cron-triggered (CloudWatch events) Lambda in AWS.

At the right time, as per the cron schedule, the Lambda tries to book the next 
 calisthenics class, and send me a Telegram message with the result.


Usage
=====
There is no HTTP interface (apart from the introspection endpoint), but just a
 cron-scheduled Lambda. So it works automatically.


Architecture
============
The main Lambda function is triggered by a cron schedule in Event Bridge, CloudWatch:
  - cron(10 19 ? * MON *) # Every Monday at 19:10 UTC (20:10/21:10AM in Rome winter/summer).
  - cron(10 19 ? * WED *) # Every Wednesday at 19:10 UTC (20:10/21:10AM in Rome winter/summer).
These times work with the business rules explained in `How it works`.

To send Telegram messages, we use Botte (part of the Patatrack monorepo) via HTTP.

No database.

![architecture-draw.io.svg](./docs/img/architecture-draw.io.svg)


How it works
============
Classes are usually booked via a mobile app that performs regular HTTP(s) requests.

I inspected these requests by installing the app on the emulator Genymotion on macOS
 and intercepting the traffic using [HTTP Toolkit](https://httptoolkit.com/docs/guides/android/).\
Find the details of these requests in the next sections.

Some business rules are in place in order to regulate bookings:
 - booking for Wednesday 20:00 classes opens the previous Monday at 20:00
 - booking for Friday 20:00 classes opens the previous Wednesday at 20:00\
So these times are the cron schedule.

1' request: login
-----------------
Login using username and password and get the `codice_sessione`.
```sh
$ curl -X POST https://reborn.shaggyowl.com/funzioniapp/v407/loginApp \
 -d "mail=rossi@gmail.com&pass=mypassword&id_sede=47" \
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

```

2' request: get palinsesto
--------------------------
Get the `id_orario_palinsesto` for the class you are interested.
You might skip this if you already know it and of it does not change over time.
```sh
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
```

3' request: book class
----------------------
Finally book the class.
```sh
$ curl -X POST https://reborn.shaggyowl.com/funzioniapp/v407/prenotazione_new \
   -d 'id_sede=47&codice_sessione=1729789529xxx&id_orario_palinsesto=719536&data=2024-10-25'
   -H "user-agent: Dart/3.1 (dart:io)"

{"status": 1, "messaggio": "Prenotazioni non aperte.", "parametri": {}}
```


Development setup
=================

---

1 - System requirements
----------------------

**Python 3.12**\
The target Python 3.12 as it is the latest available environment at AWS Lambda.\
Install it with pyenv:
```sh
$ pyenv install -l  # List all available versions.
$ pyenv install 3.12.4
```

**Poetry**\
Pipenv is used to manage requirements (and virtual environments).\
Read more about Poetry [here](https://python-poetry.org/). \
Follow the [install instructions](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions).

**Pre-commit**\
Pre-commit is used to format the code with black before each git commit:
```sh
$ pip install --user pre-commit
# On macOS you can also:
$ brew install pre-commit
```

2 - Virtual environment and requirements
----------------------------------------

Create a virtual environment and install all deps with one Make command:
```sh
$ make poetry-create-env
# Or to recreate:
$ make poetry-destroy-and-recreate-env
# Then you can open a shell and/or install:
$ poetry shell
```

Without using Makefile the full process is:
```sh
# Activate the Python version for the current project:
$ pyenv local 3.12.4  # It creates `.python-version`, to be git-ignored.
$ pyenv which python
~/.pyenv/versions/3.12.4/bin/python

# Now create a venv with poetry:
$ poetry env use ~/.pyenv/versions/3.12.4/bin/python
# Now you can open a shell and/or install:
$ poetry shell
# And finally, install all requirements:
$ poetry install
```

To add a new requirement:
```sh
$ poetry add requests
$ poetry add pytest --dev  # Dev only.
$ poetry add requests[security,socks]  # With extras.


3 - Pre-commit
--------------

```sh
$ pre-commit install
```


Deployment
==========

---

### 0. Create API in Strava

To get API keys you need to create and API App in Strava.\
Note that you can create only 1 app.\
Go to: [https://www.strava.com/settings/api]()
and create a new API.\
Take note of the `client_id` and `client_secret`.\
The script `scripts/configure_parameter_store.py` that you will run in a later step
 will guide you to get a valid access token.\
Also note that the access token in that page ("Your Access Token") is NOT what you need
 here because it has a read-only scope.\
See screenshot:
![Strava app](docs/img/3.png "Strava app")

### 1. Install deployment requirements

The deployment is managed by Serverless. Serverless requires NodeJS.\
Follow the [install instructions](https://github.com/nvm-sh/nvm#install--update-script) for NVM (Node Version Manager).\
Then:
```shell
$ nvm install --lts
$ node -v > .nvmrc
```
Follow the [install instructions](https://serverless.com/framework/docs/getting-started#install-as-a-standalone-binary)
for Serverless, something like `curl -o- -L https://slss.io/install | bash`.
We currently use version 3.12.0, if you have an older major version you can upgrade Serverless with: `sls upgrade --major`.

Then to install the Serverless plugins required:
```shell
#$ sls upgrade  # Only if you are sure it will not install a major version.
$ nvm install
$ nvm use
# You may need to restart your terminal before running the next command to avoid this warning:
#  WARN serverless-python-requirements@5.4.0 requires a peer of serverless@^2.32 || 3 but none is installed.
# The warning may eventually result in this error:
#  Error: Cannot find module '/hdmap-web/projects/job-scheduler/node_modules/es5-ext/-e'
$ sls plugin install -n serverless-python-requirements
$ sls plugin install -n serverless-iam-roles-per-function
# If it fails again try with:
$ npm install
```

### 2. Deployments steps

#### 2a. AWS Parameter Store
Add to AWS Parameter Store the Reborn app creds.\
Keys:
 - `/reborn-automator/production/reborn-creds-username`
 - `/reborn-automator/production/reborn-creds-password`

#### 2b. Actual deploy
Note: AWS CLI and credentials should be already installed and configured.\

Finally, deploy to **PRODUCTION** in AWS with:
```sh
$ sls deploy
# $ make deploy  # Alternative.
```

To deploy a single function (only if it was already deployed):
```sh
$ sls deploy function -f endpoint-health
```


Deploy to a DEV STAGE
---------------------
Pick a stage name: if your name is Jane then the best format is: `dev-jane`.\
Create the keys in AWS Parameter Store with the right stage name.

To deploy your own **DEV STAGE** in AWS version:
```sh
# Deploy:
$ sls deploy --stage dev-jane
# Delete completely when you are done:
$ sls remove --stage dev-jane
```


Copyright
========
Copyright puntonim (https://github.com/puntonim). No License.
