# Wikidata ZH Hackathon 2019

[Work in progress](#work-in-progress-24112019) <br>
[Code](#code) <br>
[Data sources](#data-sources) <br>
[Statistical Definitions](#statistical-definition) <br>
[Sceenshots](#screenshots) <br>

[Observable notebook with visualization of available data](https://observablehq.com/@rkaravia/municipalities-of-zurich-population-over-time)

We combine challenge 4 and 6. Our goal is to update the population of in wikidata based on open statistical data by the Kanton and the City of Zurich. 

Team: Katharina Kaelin, Roman Karavia, Sebastian Windeck, Philipp Rütimann, Matthias Mazenauer, Michael Grüebler 

## Work in Progress 24.11.2019 

![Dataflow](https://github.com/mmznrSTAT/wikidataZH_2019/blob/master/images/dataflow.jpg "Dataflow")

![Kanban](https://github.com/mmznrSTAT/wikidataZH_2019/blob/master/images/kanban.jpg "Kanban")

## Code

### Prerequisites

You will need python 3 and pip installed on your machine.

### Install

Execute the steps below in a terminal.

1. Create a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

```bash
python -m venv .venv
```

2. Activate the virtual environment

```bash
source .venv/bin/activate
```

3. Install the dependencies

```bash
pip install -r requirements.txt
```

### Run

Run the Jupyter Notebook (work in progress)

```bash
jupyter notebook ProjectUpdate.ipynb
```

Run one of the python scripts, for example `compare_data.py`:

```bash
python compare_data.py
```

## Data Sources

### Population of Municipalities in the Canton of Zurich 
Dataset description: Einwohnerbestand Ende Jahr nach zivilrechtlichem Wohnsitz (ab 2010 inkl. vorläufig Aufgenommene, die seit mehr als einem Jahr in der Gemeinde leben, aber ohne Wochenaufenthalter und Asylbewerber)

Get Data as csv from Canton of Zurich via API
https://www.web.statistik.zh.ch:8443/gp/GP?type=EXPORT&indikatoren=133&raumtyp=1&text=yes

Data Format: JSON or CSV

Attributes: 

Filter indikatoren=133 Bevölkerungs Personen / raumtyp=1 Alle Gemeinden

| Technical Name   | Fiel Description         | Definition  |
| ---------------- | ------------------------ | ----------- |
| RAUMEINHEIT_ID   | ID der Gemeinde          |          |
| DATEN_VORHANDEN  | true/false Datenstand    | true/false für Datenstand |
| RAUMEINHEIT_NAME | Gemeindename             | Name der Gemeinde  |
| BFS              | BFS Gemeindenummer       | Eindeuteige Gemeindenummer der Gemeinde gemäss BFS |
| ALLE_WERTE       | Anzahl Personen pro Jahr |  |

License: Open use. Must provide the source. 

Source: https://opendata.swiss/de/dataset/bevolkerung-pers

### Population of the City of Zurich
Dataset description: Wirtschaftliche Wohnbevölkerung der Stadt Zürich nach Statistischem Stadtquartier und Jahr, seit 1970. Datenqualität: 1970 – 1992 Fortschreibungsergebnisse, seit 1993 Bestand gemäss Register des Personenmeldeamtes.
https://data.stadt-zuerich.ch/dataset/bev_bestand_jahr_quartier_seit1970_od3240/resource/570f006e-2f2a-4b1f-9233-c4916c753475

Data Format: CSV

Attributes: 

| Technical Name  | Fiel Description            | Definition  |
| --------------- | --------------------------- | ----------- |
| StichtagDatJahr | Ereignisjahr                | Jahr         |
| QuarSort        | Stadtquartier (Sort)        | Offizielle ID des Statistischen Stadtquartiers (Integer) |
| QuarLang        | Stadtquartier               | Name des Statistischen Stadtquartiers (String) |
| AnzBestWir      | Wirtschaftliche Bevölkerung | Wirtschaftlich anwesende Personen (Integer) |

License: Creative Commons CCZero

Source: https://data.stadt-zuerich.ch/dataset/bev_bestand_jahr_quartier_seit1970_od3240

### Mapping of Quarters to wikidata Entitites

Dataset description: Matchingtabelle Quartiernummern zu Wikidata-ID. Diese Liste wurde am Wikimedia Hackathon 2014 in Zürich erstellt. Sie dient zur Verknüpfung zwischen statistischen Quartiernummern und den Wikidata-Item-IDs.

https://data.stadt-zuerich.ch/dataset/matchingtab-quartnr-wikidataid/resource/0090f2ed-1df9-4953-9561-5d413fd74758

Data Format: CSV

| Technical Name  | Fiel Description   | Definition  |
| --------------- | ------------------ | ----------- |
| QNr             | Quartiernummer     | Offizielle ID der statistischen Quartiere    |
| QName           | Quartiername       | Offizieller Name der statistischen Quartiere |
| DataItemID      | DataItemID         | Offizielle ID der Statistischen Quartiere für Wikidata |

License: Creative Commons CCZero

Source: https://data.stadt-zuerich.ch/dataset/matchingtab-quartnr-wikidataid


## Statistical Definition

The canton uses the "ständige" and the city of zurich the "wirtschaftliche" definition to count the population.

![Bevoelkerungsdefinition](https://github.com/mmznrSTAT/wikidataZH_2019/blob/master/images/bevoelkerungsdefinition.png "Bevoelkerungsdefinition")

More about this definition: https://www.stadt-zuerich.ch/prd/de/index/statistik/themen/bevoelkerung/bevoelkerungsentwicklung/bevoelkerungsdefinition.html

## Wikidata Definition

Important Identifiers in Wikidata (SPARQL terminology):

| Name                 | Wikidata ID   |
| -------------------- | ------------- | 
| Stadt Zürich         | Q72           | 
| Population           | P1082         | 
| Quartier             | Q19644586     | 
| Gemeinde             | Q70208        |
| im Kanton ZH         | Q11943        |
| Date (Year)          | P585          |
| URL der Fundstelle   | P854          |
| Determination method | P459          |
| Statistik            | Q12483        |
| Preferred Rank       | wikibase:rank |

Source for Gemeinden:<br> https://statistik.zh.ch/internet/justiz_inneres/statistik/de/daten/gemeindeportraet_kanton_zuerich.html#a-content 

Source for Quartiere:<br>
https://data.stadt-zuerich.ch/dataset/bev_bestand_jahr_quartier_seit1970_od3240

## Limitations

- Only municipalities are updated, which are currently active (source: geo.admin.ch)
- If a wikidata entry with a date other than 31. dec exists (eg. 1.1.2017 or 2017), a new entry will be made anyway
- For the City of Zurich only Quartiere are selected but not Kreise 
- The bot does not yet work and the current code will delete all population data before inserting the new record

## Screenshots

Manual run of the bot only for the Quarter Höngg

![Höngg Wikidata](https://github.com/mmznrSTAT/wikidataZH_2019/blob/master/images/result_wikidata_hoengg.png "Höngg Wikidata")

![Höngg Wikipedia](https://github.com/mmznrSTAT/wikidataZH_2019/blob/master/images/result_wikipedia_hoengg.png "Höngg Wikipedia")

![Höngg Siri](https://github.com/mmznrSTAT/wikidataZH_2019/blob/master/images/result_siri_hoengg.png "Höngg Siri")


## Code

(city_of_zurich.py)[https://paws.wmflabs.org/paws/user/Kalakaru/edit/wikidataZH_2019/city_of_zurich.py]

(compare_data.py)[https://paws.wmflabs.org/paws/user/Kalakaru/edit/wikidataZH_2019/compare_data.py]

(insert_wikidata.py)[https://paws.wmflabs.org/paws/user/Kalakaru/edit/wikidataZH_2019/insert_wikidata.py]

(ProjectUpdate.ipynb)[https://paws.wmflabs.org/paws/user/Kalakaru/notebooks/wikidataZH_2019/ProjectUpdate.ipynb]

(WikiBot.ipynb)[https://paws.wmflabs.org/paws/user/Kalakaru/notebooks/wikidataZH_2019/WikiBot.ipynb]



