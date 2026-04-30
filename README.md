# Real Estate Price Prediction

This project is a full-stack web application that predicts Bangalore real estate prices using machine learning.

## Overview

* Predicts property prices based on area, location, number of bedrooms, and bathrooms.
* Uses a saved scikit-learn Linear Regression model.
* Serves the browser client and Flask API from the same app for easier deployment.

## Features

* Data preprocessing: cleaning, outlier removal, and feature engineering.
* Model training: GridSearchCV and k-Fold Cross Validation.
* Frontend: HTML, CSS, and JavaScript.
* Backend: Python Flask API.
* Production entrypoint: Gunicorn with a `Procfile`.
* Health check endpoint: `GET /health`.

## Tech Stack

* Python, Pandas, NumPy, scikit-learn.
* Flask, Gunicorn.
* HTML, CSS, JavaScript.
* AWS EC2 or any Procfile/Gunicorn-compatible host.

## Run Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python server/server.py
```

Open `http://127.0.0.1:5000`.

## Production

The app is WSGI-ready through Gunicorn:

```bash
gunicorn server.server:app
```

Platforms that support Procfiles can use:

```bash
web: gunicorn server.server:app
```

## Project Structure

```text
├── client/               # Frontend files
├── server/               # Flask backend and model artifacts
├── model/                # Notebook and model files
├── requirements.txt      # Python dependencies
├── Procfile              # Production process command
```

## Dataset

* Source: Kaggle Bangalore Home Prices Dataset.

## Author

Umar Farook

Built as part of a complete Data Science learning project combining data preprocessing, ML modeling, and full-stack deployment.
