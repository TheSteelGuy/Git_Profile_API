# Coding Challenge App

## Git Profile Challenge

## Install:

```clone the repo
   $ git clone https://github.com/TheSteelGuy/Git_Profile_API.git
```

You can use a virtual environment (conda, venv, etc):
```
conda env create -f environment.yml
source activate user-profiles
```

Or just pip install from the requirements file
``` 
pip install -r requirements.txt
```
### NB I did not Use Conda(The below is what I used to Run The app)

- if you don't have virtualenv install it with
```
$ pip install virtualenv
```
```
create a virtualenv 
$ virtualenv -p python3.6 venv 
$ cd venv
$ source bin/activate
$ git clone https://github.com/TheSteelGuy/Git_Profile_API.git
$ cd Git_Profile_API
```

## Running the code


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
## Running tests

```simply on the root of the application(Git_Profile_API directory)
   $ pytest
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
watchers endpoint. This I can improve on by finding ways to to send these requests at once if possible
- Writing unit more test cases 
- Refactor the code especially request_helper.py there are some repeated operations



