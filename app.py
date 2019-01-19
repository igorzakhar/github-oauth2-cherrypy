import os
import pathlib

import cherrypy
from jinja2 import Environment, FileSystemLoader
from requests_oauthlib import OAuth2Session


env = Environment(loader=FileSystemLoader('templates'))


class GithubOAuthApp:

    @cherrypy.expose
    def index(self):
        github = OAuth2Session(cherrypy.config['client_id'])
        authorization_url, state = github.authorization_url(
            cherrypy.config['auth_base_url']
        )

        cherrypy.session['oauth_state'] = state

        raise cherrypy.HTTPRedirect(authorization_url)

    @cherrypy.expose
    def callback(self, code='', state=''):
        github = OAuth2Session(
            cherrypy.config['client_id'],
            state=cherrypy.session.get('oauth_state')
        )

        request_url = cherrypy.url(qs=cherrypy.request.query_string)
        token = github.fetch_token(
            cherrypy.config['token_url'],
            client_secret=cherrypy.config['client_secret'],
            authorization_response=request_url
        )

        cherrypy.session['oauth_token'] = token

        raise cherrypy.HTTPRedirect('/profile')

    @cherrypy.expose
    def profile(self):
        if cherrypy.session.get('oauth_token') is None:
            raise cherrypy.HTTPRedirect('/')

        github = OAuth2Session(
            cherrypy.config['client_id'],
            token=cherrypy.session.get('oauth_token')
        )
        user_data = github.get('https://api.github.com/user')
        if user_data.json().get('message') == 'Requires authentication':
            raise cherrypy.HTTPRedirect('/')

        tmpl = env.get_template('index.html')
        avatar_url = user_data.json().get('avatar_url')
        login = user_data.json().get('login')
        return tmpl.render(
            avatar_url=avatar_url,
            login=login
        )


if __name__ == '__main__':
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    config = {
        'global':
            {
                'server.socket_port': 5000,
                'tools.sessions.on': True,
                'auth_base_url': 'https://github.com/login/oauth/authorize',
                'token_url': 'https://github.com/login/oauth/access_token',
                'client_id': os.environ.get('OAUTH_CLIENT_ID'),
                'client_secret': os.environ.get('OAUTH_CLIENT_SECRET')
            },
        '/':
            {
                'tools.staticdir.root': str(
                    pathlib.Path(__file__).absolute().parent
                )
            },
        '/static':
            {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': 'static'
            }
    }

    cherrypy.quickstart(GithubOAuthApp(), config=config)
