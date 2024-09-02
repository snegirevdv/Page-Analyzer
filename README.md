# Page Analyzer

[![Continuous deployment](https://github.com/snegirevdv/Page-Analyzer/actions/workflows/main.yml/badge.svg)](https://github.com/snegirevdv/Page-Analyzer/actions/workflows/main.yml)
[![Code Climate](https://api.codeclimate.com/v1/badges/dd67028fa215d2e57ab1/maintainability)](https://codeclimate.com/github/snegirevdv/Page-Analyzer/maintainability)

Page Analyzer is a simple web application that allows users to check web pages for SEO-related issues and improvements. It helps you analyze and enhance your website's performance by checking for various factors that influence SEO rankings.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
  - [Direct Installation](#direct-installation)
  - [Using Docker Compose](#using-docker-compose)
- [Usage](#usage)
- [Example](#example)

## Features

- Analyzes web pages for SEO-related issues
- Checks for HTML structure, keywords, and other SEO factors
- Provides a user-friendly web interface
- Stores analyzed pages in a database

## Requirements

Direct installation:

- Python 3.8+
- Poetry
- PostgreSQL

Docker installation:

- Docker
- Docker Compose

## Installation

### Direct Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/snegirevdv/Page-Analyzer.git
   ```

2. Change the directory:

   ```sh
   cd Page_Analyzer
   ```

3. Create a `.env` file with the necessary environment variables and update the .env file with your configuration:

   ```sh
   touch .env
   ```

4. Install the dependencies and initialize the database:

   ```sh
   make build
   ```

5. Run the application:
   ```sh
   make start
   ```

### Using Docker Compose

1. Download the `docker-compose.production.yml` file:

   ```sh
   curl -O https://raw.githubusercontent.com/snegirevdv/Page-Analyzer/main/docker-compose.production.yml
   ```

2. Create a `.env` file with the necessary environment variables and update the .env file with your configuration:

   ```sh
   touch .env
   ```

3. Start the application using the production Docker Compose file. The application should now be running at `http://localhost:5001`:

   ```sh
   docker-compose -f docker-compose.production.yml up
   ```

## Usage

1. Start the web server.
2. Open your web browser and navigate to `http://localhost:5001` (or your domain).
3. Enter the URL of the web page you want to analyze and click the button.
4. Click the check button.
5. View the analysis results and suggested improvements.

## Example

[https://task-manager.snegirev.dev](https://task-manager.snegirev.dev/)
