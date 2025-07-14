
# Real Estate Price Prediction \u2013 Bangalore Home Prices

A full‑stack data science project that walks through the **end‑to‑end process** of building, serving and deploying a real‑estate price prediction system for Bangalore, India.

* **Model** Linear Regression (with GridSearchCV & k‑fold CV) trained on the Kaggle *Bangalore Home Prices* dataset.
* **Backend** Python + Flask REST API that loads the trained model and returns price predictions.
* **Frontend** Vanilla HTML/CSS/JavaScript single‑page UI for users to input property details.
* **DevOps** Deployed on AWS EC2 behind **Nginx**; CI‑ready project tree for rapid iteration.

---

## Table of Contents

1. [Demo](#demo)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Dataset](#dataset)
5. [Project Structure](#project-structure)
6. [Quick Start (Local)](#quick-start-local)
7. [Training the Model](#training-the-model)
8. [Running the Flask API](#running-the-flask-api)
9. [Deploying to AWS EC2](#deploying-to-aws-ec2)
10. [API Reference](#api-reference)
11. [Contributing](#contributing)
12. [License](#license)

---

## Demo <a id="demo"></a>

![Screenshot](docs/demo.png)

> **Live URL:** *Add your EC2 public DNS or Netlify link here once deployed.*

---

## Features <a id="features"></a>

* **Data Wrangling & Cleaning** using Pandas (duplicate removal, missing‑value imputation).
* **Outlier Detection & Removal** with IQR rules and domain‑specific sanity checks.
* **Feature Engineering** (e.g. converting total\_sqft ranges, creating price\_per\_sqft).
* **Dimensionality Reduction** via PCA to mitigate multicollinearity.
* **Model Selection & Hyper‑Parameter Tuning** with `GridSearchCV`.
* **10‑Fold Cross‑Validation** for robust generalisation metrics (MAE / RMSE).
* **Pickled Model Artefact** for fast, deterministic inference.
* **REST API** at `/api/predict` \u2014 accepts JSON or form‑data and responds in milliseconds.
* **Responsive Web UI** that consumes the API and displays predicted price instantly.
* **One‑Click Cloud Deployment** guide (Ubuntu 20.04 + Nginx + Gunicorn/Flask + systemd).

---

## Tech Stack <a id="tech-stack"></a>

| Layer          | Technology                                              |
| -------------- | ------------------------------------------------------- |
| Language       | **Python 3.10**, JavaScript (ES6), HTML 5, CSS 3        |
| Core Libraries | **Pandas**, **NumPy**, **scikit‑learn**, **Matplotlib** |
| Model          | Linear Regression (best RMSE \u2248 *X.X lakhs*)        |
| Serving        | **Flask** (REST), **Gunicorn** (optional)               |
| DevOps         | **AWS EC2**, **Nginx**, SSH, systemd                    |
| Tools          | JupyterLab, VS Code, PyCharm                            |

---

## Dataset <a id="dataset"></a>

* **Source:** [Bangalore Home Prices | Kaggle](https://www.kaggle.com/datasets/amitabhajoy/bengaluru-house-price-data)
* 13 input features / 13,320 rows.
* Licence: CC0 (public domain) \u2014 free for research & commercial use.

---

## Project Structure <a id="project-structure"></a>

```text
BangaloreHomePrices/
├── client/                 # Front‑end static files
│   ├── app.html
│   ├── app.js
│   └── styles.css
├── data/
│   └── Bengaluru_House_Data.csv
├── notebooks/              # EDA + model training notebooks
│   └── 01_model_build.ipynb
├── server/
│   ├── util.py             # Helper functions (load artefacts, preprocess)
│   ├── model.py            # Training / pickle dump script
│   ├── server.py           # Flask API entry‑point
│   └── requirements.txt
├── scripts/                # DevOps helpers (systemd, nginx conf)
└── README.md
```

---

## Quick Start (Local) <a id="quick-start-local"></a>

```bash
# 1. Clone repository
$ git clone https://github.com/<your‑handle>/BangaloreHomePrices.git
$ cd BangaloreHomePrices

# 2. Create virtual environment
$ python3 -m venv venv && source venv/bin/activate

# 3. Install Python dependencies
$ pip install -r server/requirements.txt

# 4. Launch Jupyter and explore notebooks (optional)
$ jupyter lab
```

---

## Training the Model <a id="training-the-model"></a>

```bash
# From project root
$ python server/model.py --retrain   # Saves model.pkl & columns.json in server/artifacts/
```

Key training flags:

| Flag          | Description                              | Default |
| ------------- | ---------------------------------------- | ------- |
| `--retrain`   | Force retraining even if artefact exists | `False` |
| `--test-size` | Test split ratio                         | `0.2`   |
| `--k-folds`   | Cross‑validation folds                   | `10`    |

---

## Running the Flask API <a id="running-the-flask-api"></a>

```bash
$ python server/server.py  # Runs on http://127.0.0.1:5000
```

Open `client/app.html` in any browser and test locally.

---

## Deploying to AWS EC2 <a id="deploying-to-aws-ec2"></a>

1. **Create EC2 instance** (Ubuntu 20.04, t2.micro is fine) and *open ports 22 & 80* in the Security Group.
2. **SSH into server**

   ```bash
   $ ssh -i "~/key.pem" ubuntu@ec2-xx-xx-xx-xx.compute-1.amazonaws.com
   ```
3. **Install system packages**

   ```bash
   $ sudo apt update && sudo apt install -y python3-pip nginx git
   ```
4. **Clone repo & install Python deps**

   ```bash
   $ git clone https://github.com/<your‑handle>/BangaloreHomePrices.git
   $ cd BangaloreHomePrices && pip3 install -r server/requirements.txt
   ```
5. **Run Flask (or Gunicorn)**

   ```bash
   $ nohup python3 server/server.py &    # quick‑and‑dirty
   ```
6. **Nginx reverse‑proxy**

   ```nginx
   # /etc/nginx/sites-available/bhp.conf
   server {
       listen 80;
       server_name _;
       root /home/ubuntu/BangaloreHomePrices/client;
       index app.html;

       location /api/ {
           rewrite ^/api(.*) $1 break;
           proxy_pass http://127.0.0.1:5000;
       }
   }
   ```

   ```bash
   $ sudo ln -s /etc/nginx/sites-available/bhp.conf /etc/nginx/sites-enabled/
   $ sudo nginx -t && sudo systemctl restart nginx
   ```
7. **Visit** `http://<EC2‑Public‑DNS>` \u2014 you should see the web app live!

---

## API Reference <a id="api-reference"></a>

### `POST /api/predict`

| Field        | Type     | Description          |
| ------------ | -------- | -------------------- |
| `location`   | `string` | Area/locality name   |
| `total_sqft` | `float`  | Total square footage |
| `bhk`        | `int`    | No. of bedrooms      |
| `bath`       | `int`    | No. of bathrooms     |

**Sample Request**

```bash
curl -X POST http://localhost:5000/api/predict \
     -H "Content-Type: application/json" \
     -d '{"location":"Indira Nagar","total_sqft":1200,"bhk":3,"bath":2}'
```

**Sample Response**

```json
{
  "estimated_price": 175.45  // in Lakh INR
}
```

---

## Contributing <a id="contributing"></a>

Pull requests are welcome! Please open an issue first to discuss what you would like to change.

---

## License <a id="license"></a>

[MIT](LICENSE)
