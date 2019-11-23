import pandas as pd
import requests
import zipfile
import os
import shutil
from SPARQLWrapper import SPARQLWrapper, JSON, XML
import logging


def import_wikidata_kt():
    """
    Generates a SPARQL query and converts this data to pandas datadframe
    :return: pd.Dataframe['wikidata_id','date','population','qualifier']
    """
    # Q70208 Gemeinde
    # Q11943 Kanton Zürich
    # P1082 Einwohner
    # P585 Zeitmpunkt
    query = """
        SELECT ?wikidata_id ?bfs_id ?date ?population ?qualifier
            WHERE
            {

              ?wikidata_id wdt:P31 wd:Q70208.
              ?wikidata_id wdt:P131 wd:Q11943.
              ?wikidata_id p:P1082 ?myvalue.
              ?wikidata_id wdt:P771 ?bfs_id.
              ?myvalue pq:P585 ?date.
              ?myvalue ps:P1082 ?population.
              ?myvalue wikibase:rank ?qualifier.
              SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }
        """

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent = "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    result = results['results']['bindings']

    population = []
    for p in result:
        mon = {
            'wikidata_id': p['wikidata_id']['value'].replace('http://www.wikidata.org/entity/', ''),
            'bfs_id' : p['bfs_id']['value'],
            'date': p['date']['value'],
            'population': p['population']['value'],
            'qualifier': p['qualifier']['value'].replace('http://wikiba.se/ontology#', ''),
        }
        population.append(mon)


    pop = pd.DataFrame(population)
    pop['date'] = pop.date.str.slice(0, 10)
    pop['bfs_id'] = pop['bfs_id'].astype(int)
    logging.info('Import Wikidata: extracted {0} entries successful'.format(pop['date'].count()))
    return pop

def import_wikidata_qt():
    """
    Generates a SPARQL query and converts this data to pandas datadframe
    :return: pd.Dataframe['wikidata_id','date','population','qualifier']
    """
    # Q19644586 Quartier
    # P1082 Einwohner
    # P585 Zeitmpunkt
    query = """
        SELECT ?wikidata_id ?date ?population ?qualifier
            WHERE
            {

              ?wikidata_id wdt:P31 wd:Q19644586.
              ?wikidata_id p:P1082 ?myvalue.
              ?myvalue pq:P585 ?date.
              ?myvalue ps:P1082 ?population.
              ?myvalue wikibase:rank ?qualifier.
              SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
            }
        """

    sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent = "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36")
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    result = results['results']['bindings']

    population = []
    for p in result:
        mon = {
            'wikidata_id': p['wikidata_id']['value'].replace('http://www.wikidata.org/entity/', ''),
            'date': p['date']['value'],
            'population': p['population']['value'],
            'qualifier': p['qualifier']['value'].replace('http://wikiba.se/ontology#', ''),
        }
        population.append(mon)


    pop = pd.DataFrame(population)
    pop['date'] = pop.date.str.slice(0, 10)
    logging.info('Import Wikidata: extracted {0} entries successful'.format(pop['date'].count()))
    return pop


def import_kantonZH_api():
    URL = "https://www.web.statistik.zh.ch:8443/gp/GP?type=EXPORT&indikatoren=133&raumtyp=1&export=csv"

    r = requests.get(url=URL)
    try:
        os.mkdir('data')
    except OSError as ex:
        print(ex)

    open('data/dataKt.zip', 'wb').write(r.content)
    zfile = zipfile.ZipFile('data/dataKt.zip')
    with zipfile.ZipFile('data/dataKt.zip', 'r') as f:
        names = f.namelist()

    df = pd.read_csv(zfile.open(names[0]), sep=';')
    df = df.iloc[:, :-1]
    df = pd.melt(df, id_vars=[df.columns[0],df.columns[1]], value_vars=df.columns[2:])
    df = df.rename(columns={"value": "population", "variable":"date"})
    df['date'] = df['date'].astype('str')+ '-12-31'

    zfile.close()
    shutil.rmtree('data')
    logging.info('Import Kanton data: extracted {0} entries successful'.format(df['BFS_NR'].count()))
    return df


def import_geoadmin_wikidata_kt():
    """
    Validation of BFS number: Checks which BFS numbers are active between geo.admin and wikidata
    :return:
    """
    endpoint_url = "https://ld.geo.admin.ch/query"

    query = """
    PREFIX schema: <http://schema.org/>
    PREFIX gn: <http://www.geonames.org/ontology#>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX geo: <http://www.opengis.net/ont/geosparql#>
    PREFIX dct: <http://purl.org/dc/terms/>
    PREFIX st: <https://ld.geo.admin.ch/def/>

    select ?Municipality ?Name ?Population ?bfs ?date ?wikidata_id
    where{
    ?Municipality gn:featureCode gn:A.ADM3 .
    ?Municipality schema:name ?Name .
    ?Municipality gn:population?Population .
    ?Municipality st:bfsNumber ?bfs .
    ?Municipality dct:issued ?date .
    ?Municipality gn:parentADM1 ?InCanton .
    ?InCanton schema:name ?CantonName .
    #?Municipality geo:hasGeometry ?Geometry .
    #?Geometry geo:asWKT ?WKT .

    #FILTER (?date = '2019-01-01'^^xsd:date)
    FILTER (?CantonName = 'Zürich')

    {SELECT DISTINCT (xsd:integer(?bfsWD) AS ?bfs)?wikidata_id ?Image WHERE {
    SERVICE <https://query.wikidata.org/bigdata/namespace/wdq/sparql>

    {
    ?wikidata_id wdt:P771 ?bfsWD .
    ?wikidata_id wdt:P31 wd:Q70208 .
    #OPTIONAL { ?wikidata_id wdt:P18 ?Image. } .
    }
    }
    }
    }
    """

    def get_results(endpoint_url, query):
        sparql = SPARQLWrapper(endpoint_url,
                               agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.75 Safari/537.36")
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        return sparql.query().convert()

    results = get_results(endpoint_url, query)
    result = results["results"]["bindings"]

    population = []
    for p in result:
        mon = {'Municipality': p['Municipality']['value'], 'Name': p['Name']['value'],
               'Population': p['Population']['value'], 'bfs': p['bfs']['value'], 'date': p['date']['value'],
               'wikidata_id': p['wikidata_id']['value'],
               'wikidata_id': p['wikidata_id']['value'].replace('http://www.wikidata.org/entity/', '')  # ,
               # 'date': p['date']['value'],
               }
        population.append(mon)

    pop = pd.DataFrame(population)

    return pop

_population_resource_id = "570f006e-2f2a-4b1f-9233-c4916c753475"
_mapping_resource_id = "0090f2ed-1df9-4953-9561-5d413fd74758"


def import_cityZH_api():
    def _query_opendata_zurich(resource_id, parse_record):
        result = requests.get(f"https://data.stadt-zuerich.ch/api/3/action/datastore_search?resource_id={resource_id}")
        records = result.json()["result"]["records"]
        parsed_rows = []
        for record in records:
            parsed_rows.append(parse_record(record))
        return parsed_rows

    def _parse_population(record):
        return {"id": record["QuarSort"], "name": record["QuarLang"], "date": f"{record['StichtagDatJahr']}-12-31",
            "population": record["AnzBestWir"], }

    def _parse_mapping(record):
        return {"id": record["QNr"], "wikidata_id": record["DataItemNr"]}

    def _apply_wikidata_mapping(mapping_rows, population_rows):
        mapping_dict = {row["id"]: row["wikidata_id"] for row in mapping_rows}
        for population_row in population_rows:
            population_row["wikidata_id"] = mapping_dict[population_row["id"]]

    population_rows = _query_opendata_zurich(_population_resource_id, _parse_population)
    mapping_rows = _query_opendata_zurich(_mapping_resource_id, _parse_mapping)
    _apply_wikidata_mapping(mapping_rows, population_rows)
    return pd.DataFrame(population_rows)


def main():
    # Database request of city/kanton level
    data_frame = import_cityZH_api().head()
    print("City of Zurich")
    print(data_frame)
    data_frame = import_kantonZH_api().head()
    print("Kanton data")
    print(data_frame)
    # Network requests
    data_frame = import_geoadmin_wikidata_kt().head()
    print("Kanton geo.admin.data")
    print(data_frame)
    data_frame = import_wikidata_kt().head()
    print("Wikidata for Kanton")
    print(data_frame)


if __name__ == "__main__":
    main()
