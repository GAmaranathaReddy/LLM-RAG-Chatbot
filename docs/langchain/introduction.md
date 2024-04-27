# Get Familiar With LangChain

Before you design and develop your chatbot, you need to know how to use LangChain. In this section, you’ll get to know LangChain’s main components and features by building a preliminary version of your hospital system chatbot. This will give you all the necessary tools to build your full chatbot.

Use your favorite code editor to create a new Python project, and be sure to create a virtual environment for its dependencies. Make sure you have Python 3.10 or later installed. Activate your virtual environment and install the following libraries:

```shell
(venv) $ python -m pip install langchain==0.1.0 openai==1.7.2 langchain-openai==0.0.2 langchain-community==0.0.12 langchainhub==0.1.14
```

You’ll also want to install [python-dotenv](https://pypi.org/project/python-dotenv/) to help you manage environment variables:

```shell
(venv) $ python -m pip install python-dotenv
```

Python-dotenv loads environment variables from .env files into your Python environment, and you’ll find this handy as you develop your chatbot. However, you’ll eventually deploy your chatbot with Docker, which can handle environment variables for you, and you won’t need Python-dotenv anymore.

If you haven’t already, you’ll need to download reviews.csv from the materials or GitHub repo for this tutorial:

Next, open the project directory and add the following folders and files:

[langchain](../assets/lanchain.png)
