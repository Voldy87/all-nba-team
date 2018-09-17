# all-nba-team
interface for a REST api about All-NBA Teams

# structure
every app (needs to be added) has its static folder, staticfiles instead collect all them for prod
## allnbateam
the project
## splashome
the presentation, which is different for every voldy87 project but not related to them (that's why it's in the root directory, i.e. at the same level of manage.py)
##  api
the api (partially Public, the others needs oauth) api/vX/..
/teams = all teams
/teams?year=2009&type=1
/records
/players
/drafts
GET /api  Accept: application/json; version=1
HTTP/1.1 401 Unauthorized
{
  'id': 'auth_failed',
  'message': "You're not logged in."
}

#deploygit ch (auto deploy heroku on master)
(in django root)
brew switch python 3.6.5
pipenv shell
[cd all_nba_team/]
django-admin compilemessages 
python3 manage.py runserver

#tech used
svg
django (i18n, dango-rest-framework)
webpack,
python (requests, kwargs, functional programming)

#models
- all