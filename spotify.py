import base64
import json
import requests
import urllib


# constant strings to use for api calls and parsing json
SPOTIFY_ARTISTS = 'artists'
SPOTIFY_ITEMS = 'items'
SPOTIFY_ID = 'id'
SPOTIFY_TRACKS = 'tracks'



# SPOTIFY BASE URL

SPOTIFY_API_BASE_URL = 'https://api.spotify.com'
API_VERSION = "v1"
SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

# USER AUTHORIZATION

# spotify endpoints
SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com/{}"
SPOTIFY_AUTH_URL = SPOTIFY_AUTH_BASE_URL.format('authorize')
SPOTIFY_TOKEN_URL = SPOTIFY_AUTH_BASE_URL.format('api/token')

# client keys
CLIENT = json.load(open('spotify_conf.json', 'r+'))
CLIENT_ID = CLIENT['id']
CLIENT_SECRET = CLIENT['secret_key']

# server side parameter
# * fell free to change it if you want to, but make sure to change in
# your spotify dev account as well *
CLIENT_SIDE_URL = "http://localhost"
PORT = 5000
REDIRECT_URI = "{}:{}/callback".format(CLIENT_SIDE_URL, PORT)
SCOPE = "playlist-modify-public playlist-modify-private"
STATE = ""
SHOW_DIALOG_bool = True
SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

# https://developer.spotify.com/web-api/authorization-guide/
auth_query_parameters = {
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
    # "state": STATE,
    # "show_dialog": SHOW_DIALOG_str,
    "client_id": CLIENT_ID
}

URL_ARGS = "&".join(["{}={}".format(key, urllib.quote(val))
                    for key, val in auth_query_parameters.iteritems()])
AUTH_URL = "{}/?{}".format(SPOTIFY_AUTH_URL, URL_ARGS)

'''
    This function must be used with the callback method present in the
    ../app.py file.
    And of course this will only works if ouath == True
'''


def authorize(auth_token):

    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": REDIRECT_URI
    }

    base64encoded = base64.b64encode("{}:{}".format(CLIENT_ID, CLIENT_SECRET))

    headers = {"Authorization": "Basic {}".format(base64encoded)}

    post_request = requests.post(SPOTIFY_TOKEN_URL, data=code_payload,
                                 headers=headers)


    # tokens are returned to the app
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]

    # use the access token to access Spotify API
    auth_header = {"Authorization": "Bearer {}".format(access_token)}
    global_header = auth_header
    print(global_header)
    return auth_header

# ARTISTS 
# https://developer.spotify.com/web-api/artist-endpoints/

GET_ARTIST_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'artists')  # /<id>



# https://developer.spotify.com/web-api/get-related-artists/
def get_related_artists(artist_id, auth_header):
    url = "{}/{id}/related-artists".format(GET_ARTIST_ENDPOINT, id=artist_id)
    resp = requests.get(url, headers=auth_header)
    return resp.json()

# https://developer.spotify.com/web-api/get-artists-top-tracks/
def get_artists_top_tracks(artist_id, auth_header, country='US'):
    url = "{}/{id}/top-tracks".format(GET_ARTIST_ENDPOINT, id=artist_id)
    myparams = {'country': country}
    resp = requests.get(url, headers=auth_header, params=myparams)
    return resp.json()

# SEARCH
# https://developer.spotify.com/web-api/search-item/

SEARCH_ENDPOINT = "{}/{}".format(SPOTIFY_API_URL, 'search')


# https://developer.spotify.com/web-api/search-item/
def search(search_type, name, auth_header):
    if search_type not in ['artist', 'track', 'album', 'playlist']:
        print 'invalid type'
        return None
    myparams = {'type': search_type}
    myparams['q'] = name
    resp = requests.get(SEARCH_ENDPOINT, headers=auth_header, params=myparams)
    return resp.json()
