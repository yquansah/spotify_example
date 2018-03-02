import requests
import urllib
import spotify
import pprint
from initialize import app, db
from flask import render_template, url_for, request, redirect, flash, session
from forms import MainForm


names = ['Kanye West', 'Jay-Z', 'Beyonce', 'Taylor Swift', 'Bruno Mars', 'Miley Cyrus', 'Kendrick Lamar', 'Drake', 'Nipsey Hussle', 'Adele']

# landing page!! lets make this really good
@app.route('/')
@app.route('/index')
def index():
	# url_args = "&".join(["{}={}".format(key,urllib.quote(val)) for key,val in auth_query_parameters.iteritems()])
	# auth_url = "{}/?{}".format(SPOTIFY_AUTH_URL, url_args)
	return redirect(spotify.AUTH_URL)
	# return render_template('index.html', r_text=result)


@app.route('/callback')
def callback():
	auth_token = request.args['code']
	auth_header = spotify.authorize(auth_token)
	session['auth_header'] = auth_header
	return redirect(url_for('main'))


# searching queries for the Spotify API
@app.route('/main', methods=['GET', 'POST'])
def main():
	main_form = MainForm()
	message = None
	# post method for main form to work with spotify API
	if main_form.validate_on_submit():
		search_name = main_form.search_name.data
		first_query = spotify.search('artist', search_name, session.get('auth_header'))


		if (len(first_query[spotify.SPOTIFY_ARTISTS][spotify.SPOTIFY_ITEMS]) == 0):
			return redirect(url_for('bad_query'))



		artist_id = first_query[spotify.SPOTIFY_ARTISTS][spotify.SPOTIFY_ITEMS][0][spotify.SPOTIFY_ID]


		


		# getting related artists for a specific artist
		second_query = spotify.get_related_artists(artist_id, session.get('auth_header'))
		rel_artists = []
		for artist in second_query[spotify.SPOTIFY_ARTISTS]:
			rel_artists.append(artist['name'])
	
		if len(rel_artists) > 10:
			rel_artists = rel_artists[:10]

		# getting top tracks for a specific artist
		third_query = spotify.get_artists_top_tracks(artist_id, session.get('auth_header'))
		top_tracks = []
		for track in third_query[spotify.SPOTIFY_TRACKS]:
			top_tracks.append(track['name'])

		if len(top_tracks) > 10:
			top_tracks = top_tracks[:10]

		db.db.artist.insert({"name":search_name, "related_artists":rel_artists, "top_tracks":top_tracks})


		return redirect(url_for('user'))
	return render_template('main.html', main_form=main_form)


# view artists currently in database
@app.route('/view_artists', methods=['GET'])
def view_artists():
	artists = db.db.artist.find()
	artists_dict = {}
	for artist in artists:
		artists_dict[artist['name']] = artist
	return render_template('view_artists.html', artists=artists_dict)

# upon user login, profile can be accessed by user
@app.route('/user')
def user():
	return render_template('success.html')



@app.route('/bad_query')
def bad_query():

	return render_template('bad_query.html')