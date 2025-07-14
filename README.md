# Real Estate Price Prediction

This project is a full-stack web application that predicts Bangalore real estate prices using machine learning.

## 🔍 Overview

* Predicts property prices based on area, location, number of bedrooms, etc.
* Built with Linear Regression and deployed using Flask and AWS EC2.

## 🧠 Features

* Data preprocessing: cleaning, outlier removal, feature engineering
* Model training: GridSearchCV, k-Fold Cross Validation
* Frontend: HTML, CSS, JavaScript
* Backend: Python Flask API
* Deployment: AWS EC2 with Nginx setup

## 🛠 Tech Stack

* Python, Pandas, NumPy, scikit-learn
* Flask, HTML/CSS/JavaScript
* AWS EC2, Nginx

## 🚀 How to Run

1. Train the model (`model_training/`)
2. Start Flask server: `python server.py`
3. Run frontend (open `index.html`)
4. Deployed version available on AWS EC2 (if configured)

## 📂 Project Structure

```
├── client/               # Frontend files
├── server/               # Flask backend files
├── model_training/       # Jupyter notebooks for training
├── requirements.txt      # Python dependencies
```

## 📡 Deployment Steps (EC2)

* Launch EC2 instance and open port 80
* Set up Nginx config for reverse proxy
* Deploy backend and frontend code to `/home/ubuntu`
* Start Flask server and access site using public EC2 URL

## 📊 Dataset

* Source: Kaggle Bangalore Home Prices Dataset

## 👤 Author

Umar Farook

---

> Built as part of a complete Data Science learning project — combining data preprocessing, ML modeling, and full-stack deployment.
