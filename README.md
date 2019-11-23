# Wikidata ZH Hackathon 2019

We combine challenge 4 and 6. Our goal is to update the population of in wikidata based on open statistical data by the Kanton and the City of Zurich. 

Team: Katharina Kaelin, Roman Karavia, Sebastian Windeck, Philipp Rütimann, Matthias Mazenauer, Michael Grüebler

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

| Name           | Wikidata ID   |
| -------------- | ------------- | 
| Stadt Zürich   | Q72           | 
| Population     | P1082         | 
| Quartier       | Q19644586     | 
| Gemeinde       | Q70208        |
| im Kanton ZH   | Q11943        |
| Date (Year)    | P585          | 
| Preferred Rank | wikibase:rank |

## Limitations

- Only municipalities are updated, which are currently active (source: geo.admin.ch)
- If a wikidata entry with a date other than 31. dec exists (eg. 1.1.2017 or 2017), a new entry will be made anyway
- For the City of Zurich only Quartiere are selected but not Kreise 

