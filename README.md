# Master Client Index

BrightHive's Master Client Index Platform.

## What is a Master Client Index

The **Master Client Index** (MCI) is a repository of the clients in a Data Trust ecosystem. The MCI stores the client information and provides a unique Master Client Index ID (MCI ID).

## Get started

### Docker

BrightHive uses Docker to ensure that developers do consistent work, across all environments. MCI comes with `Dockerfile` and `docker-compose.yml`. Use them, like so:

```
# build an image, and give it a clear name with a version/tag number
docker build -t brighthive/master-client-index:1.0.0 .

# configure and run containers (i.e., the MCI app, and psql)
docker-compose up -d
```

`docker-compose.yml` maps port 8000 (on the container) to port 8001. Visit MCI by going to `http://0.0.0.0:8001/health`. You should see a JSON blob. (Read on to learn about API access.)

```json
{
	message: "Access Denied"
}
```

### Managing the virtual environment

BrightHive recommends managing virtual environments with `pipenv`. [Learn how to setup `pipenv`.](https://docs.pipenv.org/en/latest/) Then, do the following:

```
# tell pipenv to create/update a virtual env
pipenv install

# install development dependencies, i.e., the libraries
# enumerated in [dev-packages] of the Pipfile
pipenv install --dev
```

Need to install another dependency, not included in the Pipfile? Simply run:

```
pipenv install <package name>
# e.g., pipenv install flake8
```
 
`pipenv install` automatically updates the `Pipfile` and `Pipfile.lock`. Pull these into the docker container by re-building the MCI image, and re-configuring the container:

```
docker build -t brighthive/master-client-index:1.0.0

docker-composer up -d
```

## API Access (Auth)

The MCI exposes several [RESTful endpoints](https://app.swaggerhub.com/apis-docs/BrightHive/master-client-index/1.0.0), e.g., `users/{mci_id}`. To access them, the following steps are required:

1. Retrieve Access Token from OAuth 2.0 Server.
2. Use the Access Token to make HTTP request to the API.
3. Renew the expired Token.

### Retrieve Access Token from OAuth 2.0 Server

In order to acquire an access token from the server, the client must make a request for a new token using it's assigned Client ID and Client Secret. Also, the audience and grant type (i.e. `client_credentials`) must be provided.

The Python snippet below provides an example of how to retrieve an access token.

```python
def get_test_token():
    headers = {'content-type': 'application/json'}
    data = {'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET,
            'audience': AUDIENCE, 'grant_type': 'client_credentials'}
    r = requests.post(OAUTH2_TOKEN_URL, headers=headers, data=json.dumps(data))
    token = r.json()['access_token']
    return token
```

A JSON object similar to the one below will be returned. This object will provide the access token as a JWT (`access_token`). It also provides the expiration time (in seconds), the token's scope, and the token type.

The decoded JWT will also provide details of the token's creation and expiration times.

```bash
{'access_token': 'eyA0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6Ik1EaEVSRUV6UXpBek56WkJNVGM1TVRJM05EZ3lSVEk1UlRFNVFrWkZRMFUxUlROR01qZ3pNUSJ9.eyJpc3MiOiJodHRwczovL2JyaWdodGhpdmUtdGVzdC5hdXRoMC5jb20vIiwic3ViIjoiOGYwT1lnMUJleW40NjZoaXlPSlZka3ZlRndWdm9GT2lAY2xpZW50cyIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6ODAwMCIsImlhdCI6MTU1Mzg3NDY1NSwiZXhwIjoxNTUzODc1MjU1LCJhenAiOiI4ZjBPWWcxQmV5bjQ2NmhpeU9KVmRrdmVGd1Z2b0ZPaSIsInNjb3BlIjoiZ2V0OnVzZXJzIiwiZ3R5IjoiY2xpZW50LQNyPWRlbnRpYWxzIn0.H_H7KC9VcTOE-6vcKE711CnHGQpD5Y6dNHJYGetm4DOlKf90u00eSqlc3sX5ZECF5uUVnk-SSd3yM4FxBXhrZYc7Wv3jrg0Ms2uFrAijR8-ZPB0Wlo0ig2aoyahsnzrut1Bln4d-rfzVFDfHpTo2zocRzxEBdw8VLr9MCE5ZZ4N9rj4RgjH1cV8QGKim6DtvjbCZUiQL0LF4icox3mKASW1Yekt7LtodUnJJmR3JgvaSibyQSAt0wSYe2v5kvbdMY89N4iHuJ5FTGJUIIub28inhEnsdXJUtSoBPSzfCARNjRQwaZvw05fSENfUyr8Z5kmZntW0gMKseB2X7_fJ4jQ', 'scope': 'get:users', 'expires_in': 600, 'token_type': 'Bearer'}
```

### Use the Acces Token to Make HTTP Request to the API

Once the token is retrieved, simply include it as a `Bearer` token with HTTP requests as shown in the example below.

```bash
curl -X GET https://sandbox.brighthive.net/master-client-index/users -H 'Authorization: Bearer eyA0eXAiOiJKV1QiLCJhbGci...'

```

### Renew The Expired Token

Once the token has expired, simply request a new token via the same mechanism that was used to provide the previous token.

## Data

MCI has relatively unsurprising data models. Populate your database manually, or ask a fellow developer for a db dump. With the latter, run:

```
cat <dump_name>.sql | docker exec -i masterclientindex_postgres_mci_1 psql -U brighthive -d mci_dev

# cat <filename>.sql | docker exec -i <psql_container_name> -U <username> -d <database>
```

This command ports the database dump to the psql container, in a single, easy step.

