## Setup enviroment variables

0. Add the required key-value pairs to your .env file.
   NEWSAPI_API_KEY=<your_newsapi_api_key>
   OPENAI_API_KEY=<your_openai_api_key>
   OPENAI_ORGANIZATION=<your_openai_organization>

## Installation Steps

1. Create a python venv by venv running the following command:

```
python3 -m venv venv_python_news
source venv_python_news/bin/activate
```

2. Install the required packages from requirements.txt by running the following command:

```
pip install -r requirements.txt
```

## Dependencies

- openai
- newsapi-python
- autopep8
- python-dotenv

## Usage

This program takes a single command line argument and retrieves data from different APIs based on the argument provided. The default API is ChatGPT.

The program can be run by executing the following command in the terminal:

```
python main.py <argument>
```

Replace `<argument>` with either `c` or `n`. If `c` is provided, data will be retrieved from ChatGPT API. If `n` is provided, data will be retrieved from NewsAPI. If no argument is provided, the program will assume the default value of `c` and retrieve data from ChatGPT.

### Example usage:

Retrieve data from ChatGPT (default):

```
python program.py
```

Retrieve data from ChatGPT:

```
python program.py c
```

Retrieve data from NewsAPI:

```
python program.py n
```
