import os
import pathlib
from urllib.parse import urlparse

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
    def profile(self, page=''):

        if cherrypy.session.get('oauth_token') is None:
            raise cherrypy.HTTPRedirect('/')

        github = OAuth2Session(
            cherrypy.config['client_id'],
            token=cherrypy.session.get('oauth_token')
        )

        profile_data = github.get(
            'https://api.github.com/user'
        )

        repos_url = profile_data.json().get('repos_url')
        request_url = '{}?page={}'.format(repos_url, page)

        repos_data = github.get(request_url)

        prev_link = repos_data.links.get('prev')
        prev_url_query = None
        if prev_link is not None:
            prev_url_query = urlparse(prev_link.get('url')).query

        next_link = repos_data.links.get('next')
        next_url_query = None
        if next_link is not None:
            next_url_query = urlparse(next_link.get('url')).query

        avatar_url = profile_data.json().get('avatar_url')
        login = profile_data.json().get('login')
        repos_count = profile_data.json().get('public_repos')

        tmpl = env.get_template('index.html')

        source_path = urlparse(
            'https://github.com/igorzakhar/github-oauth2-cherrypy'
        )
        author, repo_name = list(filter(bool, source_path.path.split('/')))

        return tmpl.render(
            avatar_url=avatar_url,
            login=login,
            repos_count=repos_count,
            repos_list=repos_data.json(),
            prev_url_query=prev_url_query,
            next_url_query=next_url_query,
            author_name=author,
            repo_name=repo_name,
            author_profile=cherrypy.config['author_profile'],
            source_code=cherrypy.config['source_code']
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
                'client_secret': os.environ.get('OAUTH_CLIENT_SECRET'),
                'author_profile': 'https://github.com/igorzakhar',
                'source_code': 'https://github.com/igorzakhar/github-oauth2-cherrypy'
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
