# Page Analyzer

[![Actions Status](https://github.com/snegirevdv/python-project-83/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/snegirevdv/python-project-83/actions)
[![Code Climate](https://codeclimate.com/github/snegirevdv/python-project-83.png)](https://codeclimate.com/github/snegirevdv/python-project-83.png)

Page Analyzer is a simple web application that allows users to check web pages for SEO-related issues and improvements. It helps you analyze and enhance your website's performance by checking for various factors that influence SEO rankings.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Requirements] (#requirements)
- [Usage](#usage)
- [Example](#license)

## Features
- Analyze web pages for SEO-related issues
- Check for HTML structure, keywords, and other SEO factors
- User-friendly web interface
- Database storage for analyzed pages

## Requirements
- Python 3.8+
- Poetry
- PostgreSQL

## Setup
1. Clone the repository:
    ```sh
    git clone https://github.com/snegirevdv/python-project-83.git
    ```

2. Change the directory:
    ```sh
    cd python-project-83
    ```

3. Configure the environment variables by creating a `.env` file:
    ```sh
    touch .env
    # Update the .env file with your configuration
    ```

4. Install the dependencies and initialize the database:
    ```sh
    make build
    ```

5. Run the application:
    ```sh
    make start
    ```

## Usage

1. Start the web server.
2. Open your web browser and navigate to `http://localhost:5000` (or your domain).
3. Enter the URL of the web page you want to analyze and click the button.
4. Click the check button.
5. View the analysis results and suggested improvements.
