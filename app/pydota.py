"""PyDota - A tiny Python wrapper for the Dota 2 Steam Web API.
Visit https://steamcommunity.com/dev for more information.
"""

import requests
import urllib


STEAM_API_URL = "https://api.steampowered.com/"


class PyDotaError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class PyDota(object):
    """Creates an API object using a Steam API key.

    Optional paramters:
    language=<lang>
    (see http://en.wikipedia.org/wiki/ISO_639-1 for language codes
    and http://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
    for country codes)
    """
    def __init__(self, api_key, language=None):
        self.api_key = api_key

        if language:
            self.language = language
        else:
            self.language = "en_us"

    def get_match_history(self, **kwargs):
        """Returns a dictionary with a list of recent Dota matches.

        Optional parameters:
        hero_id=<id>
        game_mode=<mode>
        skill=<skill>
        min_players=<count>
        account_id=<id>
        league_id=<id>
        start_at_match_id=<id>
        matches_requested=<n>
        tournament_games_only=<string>
        """
        url = self._create_url("IDOTA2Match_570/GetMatchHistory/v001/", **kwargs)
        return self._get(url)

    def get_match_details(self, match_id):
        """Returns a dictionary with details for a Dota Match.

        Required parameter:
        match_id=<id>
        """
        url = self._create_url("IDOTA2Match_570/GetMatchDetails/v001/", match_id=match_id)
        return self._get(url)

    def get_match_history_by_seq_num(self, **kwargs):
        """Returns a dictionary with a list of recent Dota matches in recorded order.

        Optional parameters:
        start_at_match_seq_num=<id>
        matches_requested=<n>
        """
        url = self._create_url("IDOTA2Match_570/GetMatchHistoryBySequenceNum/v0001/", **kwargs)
        return self._get(url)

    def get_heroes(self):
        """Returns a dictionary with details for heroes."""
        url = self._create_url("IEconDOTA2_570/GetHeroes/V001/")
        return self._get(url)

    def get_league_listing(self):
        """Returns a dictionary with a list of tournament leagues."""
        url = self._create_url("IDOTA2Match_570/GetLeagueListing/v0001/")
        return self._get(url)

    def get_live_league_games(self):
        """Returns a dictionary with a list of the
        tournament games that are currentely in progress.
        """
        url = self._create_url("IDOTA2Match_570/GetLiveLeagueGames/v0001/")
        return self._get(url)

    def get_team_info_by_team_id(self, **kwargs):
        """Returns a dictionary of teams that have been created in the client.

        Optional parameters:
        start_at_team_id=<id>
        teams_requested=<n>
        """
        url = self._create_url("IDOTA2Match_570/GetTeamInfoByTeamID/v001/", **kwargs)
        return self._get(url)

    def get_player_summaries(self, steamids):
        """Returns a dictionary of player information."""
        url = self._create_url("ISteamUser/GetPlayerSummaries/v0002/", steamids=steamids)
        return self._get(url)

    def get_game_items(self):
        """Returns a dictionary with details for items."""
        url = self._create_url("IEconDOTA2_570/GetGameItems/v0001/")
        return self._get(url)


    def _create_url(self, api_call, **kwargs):
        """Returns a callable API query."""
        kwargs["key"] = self.api_key
        if "language" not in kwargs:
            kwargs["language"] = self.language
        api_query = urllib.urlencode(kwargs)

        return "{0}{1}?{2}".format(STEAM_API_URL, api_call, api_query)

    @staticmethod
    def _get(url):
        """Makes a request to the url and returns the response in JSON."""
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            raise PyDotaError("The API Key you have entered is invalid.")
        elif response.status_code == 503:
            raise PyDotaError("The connection has timed out.")
        raise PyDotaError("An unknown error has occured.")


def download_hero_image(name, size, path):
    """Downloads a hero image with the specified size, and saves to path.

    Required parameters:
    name=Full name without "npc_hero_dota_"
    size=Allowed sizes are: "sb", "lg", "full"
    path=<path to save dir including the filename>
    """
    url = "http://cdn.dota2.com/apps/dota2/images/heroes/{}"
    filename = "{}_{}.png".format(name, size)
    urllib.urlretrieve(url.format(filename), path)

def download_item_image(name, path):
    """Downloads a item image and saves to path.

    Required parameters:
    name=Full name without "npc_hero_dota_"
    path=<path to save dir including the filename>
    """
    url = "http://cdn.dota2.com/apps/dota2/images/items/{}"
    filename = "{}_lg.png".format(name)
    urllib.urlretrieve(url.format(filename), path)
