
<div align="center">
<h1 align="center">
<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />
<br>songswap-insights
</h1>
<h3>Unlock Musical Insights</h3>
<h3>Developed with the software and tools listed below.</h3>

<p align="center">
<img src="https://img.shields.io/badge/Docker_Engine-20.10.21-2496ED.svg?style&logo=Docker&logoColor=2496ED" alt="Docker" />
<img src="https://img.shields.io/badge/Python-3.10.11-3776AB.svg?style&logo=Python&logoColor=3776AB" alt="Python" />
<img src="https://img.shields.io/badge/Flask-2.3.2-000000.svg?style&logo=Flask&logoColor=000000" alt="Flask" />
<img src="https://img.shields.io/badge/gunicorn-20.1.0-499848.svg?style&logo=gunicorn&logoColor=499848" alt="gunicorn" />
<img src="https://img.shields.io/badge/PostgreSQL-4169E1.svg?style&logo=postgresql&logoColor=white" alt="postgresql" />
<br>
<img src="https://img.shields.io/badge/Amazon RDS-527FFF.svg?style&logo=amazonrds&logoColor=white" alt="Amazon RDS" />
<img src="https://img.shields.io/badge/Amazon S3-569A31.svg?style&logo=amazons3&logoColor=white" alt="Amazon S3" />
<img src="https://img.shields.io/badge/Amazon EC2-FF9900.svg?style&logo=amazonec2&logoColor=white" alt="Amazon EC2" />
<img src="https://img.shields.io/badge/Amazon CloudWatch-FF4F8B.svg?style&logo=amazoncloudwatch&logoColor=white" alt="Amazon CloudWatch" />

</p>
</div>

---

## 📒 Table of Contents
- [📒 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [⚙️ Features](#-features)
- [📂 Project Structure](#project-structure)
- [🧩 Modules](#modules)
- [🚀 Getting Started](#-getting-started)
- [🗺 Roadmap](#-roadmap)

---


## 📍 Overview

This repository is a Flask backend application that provides data analytics and insights for a music sharing platform. It utilizes caching to improve performance and retrieves information such as top tracks, artists, listeners, and global music statistics from a PostgreSQL database using SQLAlchemy. The project aims to help users understand their music consumption habits and provides valuable insights to drive better human-centeric music recommendations.

---

## ⚙️ Features

| Feature                | Description                           |
| ---------------------- | ------------------------------------- |
| **⚙️ Architecture**     | The system is built using the Flask framework, following a modular design pattern with blueprints for different functionalities. It integrates with a database using `SQLAlchemy` for efficient data handling.    |
| **📖 Documentation**   | Documentation is available for environment configuration and some code files. In the future, an automated API documentation tool like Swagger or APIFairy will be used to generate documentation for the API endpoints.   |
| **🔗 Dependencies**    | The main dependency is the Flask framework for building the web application. Additional dependencies include `Flask-Caching` and `SQLAlchemy` for caching and database handling respectively.    |
| **🧩 Modularity**      | Files are organized into different modules and blueprints based on their functionalities: API endpoints, data retrieval, etc. This separation allows for code reuse, testing, and easier maintenance.   |
| **✔️ Testing**          | Testing is performed via a local Postman application. An automated test suite will be implemented in the future.   |
| **⚡️ Performance**      | Flask-Caching improves performance by reducing the both number of database queries and amount of data retrieved from AWS. This improves both page load speeds and AWS RDS usage costs.    |
| **🔐 Security**        | This API is available only to the [songswap-app](https://github.com/SongSwap-social/songswap-app) frontend. For the time being, it will not be made publicly available.   |
| **🔌 Integrations**    | This API is used by the [songswap-app](https://github.com/SongSwap-social/songswap-app) frontend application. It is responsible for retrieving data to be visualized on users' "Insights" pages.   |
| **📶 Scalability**     | There is no database sharding or replication implemented at this time. However, the application is designed to be scalable and can be deployed on multiple instances. If deployed on multiple instances, it is necessary to re-design the API to use a central caching server.   |

---


## 📂 Project Structure


```
repo
├── Dockerfile
├── app
│   ├── __init__.py
│   ├── cache
│   │   ├── __init__.py
│   │   └── decorators.py
│   ├── models
│   │   ├── __init__.py
│   │   └── history.py
│   ├── routes
│   │   ├── __init__.py
│   │   ├── cache.py
│   │   ├── insights.py
│   │   └── insights_global.py
│   └── services
│       ├── __init__.py
│       ├── insights_global_service.py
│       └── insights_service.py
├── buildspec.yml
├── config.py
├── requirements.txt
├── run.py
└── tests
    └── __init__.py

6 directories, 18 files
```

---

## 🧩 Modules

<details closed><summary>Root</summary>

| File       | Summary                                                                                                                                                                                                                                                                                          |
| ---        | ---                                                                                                                                                                                                                                                                                              |
| run.py     | Creates and runs the API by calling the `create_app()` function from the app module. The app runs on the specified port and in debug mode if the DEBUG flag is set.                                                                                                            |
| config.py  | Loads Flask-specific environment variables from a .env file. It retrieves values for DEBUG, SECRET_KEY, FLASK_RUN_PORT, SQLALCHEMY_DATABASE_URI, and CACHE_TYPE, among others, from the environment. It also sets up cache configurations and disables SQLAlchemy track modifications.         |
| Dockerfile | Sets up a Python Flask application in a Docker container. It installs necessary dependencies, sets environment variables, configures the working directory, exposes a port, and runs the application using Gunicorn. The application can be accessed externally on port 5001. |

</details>

<details closed><summary>Cache</summary>

| File          | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ---           | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| decorators.py | A decorator function that caches an endpoint's response and adds logging functionality. It allows for setting a timeout for cache expiration, a key prefix for the cache key, and a condition for bypassing caching if necessary. The function decorates the view function, checks if the response is already cached, and returns the cached value if it exists. If the response is not cached, it calls the view function, stores the result in the cache, and returns the result. |

</details>

<details closed><summary>Models</summary>

| File       | Summary                                                                                                                                                                                                                         |
| ---        | ---                                                                                                                                                                                                                             |
| history.py | Defines various models for a database schema for Spotify's tracks, artists,  and their relationships, using SQLAlchemy. It includes functionalities for managing cascading deletion of records within these tables. |

</details>

<details closed><summary>Routes</summary>

| File               | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ---                | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| cache.py           | Defines a Flask blueprint that defines two endpoints for managing a simple cache. The first endpoint clears the cache when a secret key is provided, and the second endpoint returns the current size of the cache. This code is used to test and validate the cache's functionality.                                                                                                                                                                                                                                                                     |
| insights_global.py | A Flask blueprint that defines endpoints for retrieving insights about global listening history data. These endpoints include retrieving the total number of listens, distinct tracks and artists, total listen time, and top tracks, artists, and listeners based on a specified limit. The code uses caching for performance optimization and handles validation of the limit parameter. The response is returned in JSON format with appropriate status codes. |
| insights.py        | A Flask Blueprint that defines endpoints related to user-specific insights. It includes functions to retrieve top tracks, top artists, and top primary artists for a given user. The code also includes helper functions for parsing and validating query parameters. Caching is applied to the API routes using decorators.                                                                                                                                                  |

</details>

<details closed><summary>Services</summary>

| File                       | Summary                                                                                                                                                                                                                                                                                                                                    |
| ---                        | ---                                                                                                                                                                                                                                                                                                                                        |
| insights_global_service.py | Functions to query a database using SQLAlchemy. It retrieves top tracks, top artists, top primary artists, top listeners, total listens, distinct tracks, distinct artists, distinct primary artists, and total listen time.                                                                                     |
| insights_service.py        | Functions for retrieving top tracks and artists based on user history, counting the total tracks, and distinct tracks for a given user. It utilizes SQLAlchemy queries to join tables, apply filters, and group data. There are also helper functions for printing SQL queries and handling image URLs. |

</details>

---

## 🚀 Getting Started

### ✔️ Prerequisites

Before you begin, ensure that you have the following prerequisites installed:
> - `ℹ️ docker`
> - `ℹ️ PostgreSQL`

### 📦 Installation

1. Clone the songswap-insights repository:
```sh
git clone git@github.com:SongSwap-social/songswap-insights.git
```

2. Change to the project directory:
```sh
cd songswap-insights
```

3. Install the dependencies:
```sh
pip install -r requirements.txt
```

### 🎮 Using songswap-insights

- Run the application locally, for testing or development purposes:
```sh
python main.py
```

- Run the application in a Docker container:
```sh
docker build -t songswap-insights .
docker run songswap-insights
```

---

## 🗺 Roadmap

> - [X] `ℹ️  Create user-specific insights endpoints`
> - [X] `ℹ️  Create global insights endpoints`
> - [X] `ℹ️  Add caching to endpoints`
> - [X] `ℹ️  Add logging to endpoints`
> - [] `ℹ️  Add documentation for endpoints (Swagger, APIFairy)`
> - [] `ℹ️  Add automated testing`

---
