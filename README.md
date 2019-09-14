# Coding Challenge App

A skeleton flask app to use for a coding challenge.

## Install:

You can use a virtual environment (conda, venv, etc):
```
conda env create -f environment.yml
source activate user-profiles
```

Or just pip install from the requirements file
``` 
pip install -r requirements.txt
```

## Running the code

### Spin up the service

```
# start up local server
python -m run 
```

### Making Requests with CURL

```
curl -i "http://127.0.0.1:5000/<organization>"
for example: curl -i "http://127.0.0.1:5000/pygame"
```
### Making Requests with Postman
```
send a GET request 
GET http://127.0.0.1:5000/<organization>
eg GET http://127.0.0.1:5000/pygame
```


## Typical successful Request  
```
{
  "result": {
    "languages": [
      {
        "Github": [
          {
            "c": 3
          },
          {
            "python": 4
          },
          {
            "ruby": 1
          }
        ]
      },
      {
        "Bitbucket": [
          {
            "": 1
          },
          {
            "c++": 1
          },
          {
            "python": 5
          }
        ]
      }
    ],
    "repo_types": {
      "total_forked_repos": 0,
      "total_original_repos": 15
    },
    "topics": [],
    "total_watchers": 1736
  }
}
```
## Typical of response when organization does not exist

```
{
  "result": {
    "languages": [],
    "repo_types": {
      "total_forked_repos": 0,
      "total_original_repos": 0
    },
    "topics": [],
    "total_watchers": 0
  }
}
```


## What'd I'd like to improve on...
- Current implementation sends single request at atime for all the urls to the bitbucket
watchers endpoint. This I can improve on by using asyn libraries such as iohttp.
- Writing unit tests to for various cases
- Refactor the code especially request_helper.py there are some repeated operations


