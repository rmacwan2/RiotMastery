URL = {
    'base': 'https://{proxy}.api.pvp.net/api/lol/{url}',
    'base1': 'https://{proxy}.api.pvp.net/api/lol/static-data/{region}/{url}',
    'base2': 'https://{proxy}.api.pvp.net/{url}',
    'summoner_by_name': '{region}/v{version}/summoner/by-name/{names}',
    'summoner_by_id': '{region}/v{version}/summoner/{summonerid}',
    'champion_ids': 'v{version}/champion',
    'mastery_list': 'championmastery/location/{platformid}/player/{playerid}/champions'
}

API_VERSIONS = {
    'summoner': '1.4',
    'champion': '1.2'
}

REGIONS = {
    'north_america': {'regionid': 'na',
                      'platformid': 'NA1'}
}

