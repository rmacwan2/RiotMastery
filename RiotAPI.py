import requests
import RiotConsts as Consts

class RiotAPI(object):

    def __init__(self, api_key, region=Consts.REGIONS['north_america']['regionid']):
        self.api_key = api_key
        self.region = region

    def _request(self, api_url, base, params={}):
        args = {'api_key': self.api_key}
        args = dict(list(args.items()) + list(params.items()))
        response = requests.get(
            Consts.URL[base].format(
                proxy=self.region,
                region=self.region,
                url=api_url
                ),
            params=args
            )

        print(response.url)
        return response.json()

    def get_summoner_by_name(self, name):
        api_url = Consts.URL['summoner_by_name'].format(
            region=self.region,
            version=Consts.API_VERSIONS['summoner'],
            names=name
            )
        return self._request(api_url, 'base')

    def get_summoner_by_id(self, player_id):
        api_url = Consts.URL['summoner_by_id'].format(
            region=self.region,
            version=Consts.API_VERSIONS['summoner'],
            summonerid=player_id
            )
        return self._request(api_url, 'base')

    def get_champion_ids(self):
        api_url = Consts.URL['champion_ids'].format(
            region=self.region,
            version=Consts.API_VERSIONS['champion']
            )
        params = {'locale': 'en_US', 'champData': 'info'}
        return self._request(api_url, 'base1', params)

    def get_mastery_list(self, player_id):
        api_url = Consts.URL['mastery_list'].format(
             platformid=Consts.REGIONS['north_america']['platformid'],
             playerid=player_id
        )
        return self._request(api_url, 'base2')

