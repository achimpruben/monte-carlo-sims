# Monte Carlo Simulations
**[Work in progress]**

## 🎯 Description
A simple **Python Flask application** that estimates the area/volume of geometric shapes using the **Monte Carlo random sampling method**. This is an exercise in integrating scientific computing with web development.

### Key Features
* Implements the Monte Carlo numerical method for geometric estimation.
* Logs and plots the convergence of the $\pi$ estimate over multiple runs.
* Uses Matplotlib to plot random points and the $\pi$ convergence trend.

## ⚙️ Setup

1.  **Create the Virtual Environment**
    ```bash
    python -m venv venv
    ```
2.  **Activate the Virtual Environment**
    ```bash
    venv\Scripts\activate
    ```
3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run Application**
    ```bash
    python app.py
    ```
    Navigate to the address shown in the terminal (e.g. `http://127.0.0.1:5000/`).
