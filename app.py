from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import matplotlib
matplotlib.use('Agg')  # non-GUI backend
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os, math, csv
import pandas as pd 

app = Flask(__name__)

def monte_carlo_circle_area(radius = 1.0, num_points = 10000):
    x = np.random.uniform(-radius, radius, num_points)
    y = np.random.uniform(-radius, radius, num_points)
    inside = x**2 + y**2 <= radius**2
    area_estimate = (np.sum(inside) / num_points) * (2 * radius)**2

    plt.figure(figsize=(5,5))
    plt.scatter(x[inside], y[inside], s = 1, color = 'blue', label= 'Inside')
    plt.scatter(x[~inside], y[~inside], s = 1, color = 'red', label= 'Outside')
    plt.title(f"Monte Carlo Area: {area_estimate:.4f}")
    plt.axis('equal')
    plt.legend()

    plot_path = os.path.join('static', 'plot-circle.png')
    plt.savefig(plot_path)
    plt.close()

    return area_estimate

def monte_carlo_ellipse_area(a=2.0, b=1.0, num_points=10000):
    x = np.random.uniform(-a, a, num_points)
    y = np.random.uniform(-b, b, num_points)
    inside = (x**2 / a**2) + (y**2 / b**2) <= 1
    area_estimate = (np.sum(inside) / num_points) * (2 * a) * (2 * b)

    plt.figure(figsize=(5, 5))
    plt.scatter(x[inside], y[inside], s=1, color='blue', label='Inside')
    plt.scatter(x[~inside], y[~inside], s=1, color='red', label='Outside')
    plt.title(f"Monte Carlo Ellipse Area: {area_estimate:.4f}")
    plt.axis('equal')
    plt.legend()

    plot_path = os.path.join('static', 'plot-ellipse.png')
    plt.savefig(plot_path)
    plt.close()

    return area_estimate

def monte_carlo_sphere_volume(radius=1.0, num_points=10000):
    x = np.random.uniform(-radius, radius, num_points)
    y = np.random.uniform(-radius, radius, num_points)
    z = np.random.uniform(-radius, radius, num_points)
    
    inside = x**2 + y**2 + z**2 <= radius**2
    volume_estimate = (np.sum(inside) / num_points) * (2 * radius)**3

    fig = plt.figure(figsize=(6, 5))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x[inside][:500], y[inside][:500], z[inside][:500], c='blue', s=1, label='Inside')
    ax.scatter(x[~inside][:500], y[~inside][:500], z[~inside][:500], c='red', s=1, label='Outside')
    ax.set_title(f"Monte Carlo Sphere Volume: {volume_estimate:.4f}")
    ax.legend()
    
    plot_path = os.path.join('static', 'plot-sphere.png')
    plt.savefig(plot_path)
    plt.close()

    return volume_estimate

def monte_carlo_pi_estimate(radius = 1.0, circle_area = math.pi):
    return circle_area / (radius)**2

def actual_circle_area(radius = 1.0):
    return math.pi * (radius)**2

def actual_sphere_volume(radius=1.0):
    return (4/3) * math.pi * radius**3

def log_estimate(num_points, pi_estimate):
    log_file = 'static/pi_estimates.csv'
    file_exists = os.path.isfile(log_file)

    with open(log_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['num_points', 'pi_estimate'])
        writer.writerow([num_points, pi_estimate])

def plot_pi_convergence():
    log_file = 'static/pi_estimates.csv'
    if not os.path.isfile(log_file):
        return

    df = pd.read_csv(log_file)

    plt.figure(figsize=(6, 4))
    plt.plot(df['num_points'], df['pi_estimate'], marker='o', linestyle='-', label='Estimate of π')
    plt.axhline(math.pi, color='red', linestyle='--', label='Actual π')
    plt.xlabel('Number of Points')
    plt.ylabel('Estimated π')
    plt.title('Convergence of Monte Carlo π Estimate')
    plt.legend()
    plt.grid(True)
    plt.savefig('static/pi_convergence.png')
    plt.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/circle', methods=['GET', 'POST'])
def circle():
    area = pi_estimate = actual_area = None
    
    if request.method == 'POST':
        try:
            num_points = int(request.form['num_points'])
            rad_num = float(request.form['rad_num'])
            
            if num_points > 0 and rad_num > 0:
                area = monte_carlo_circle_area(radius = rad_num, num_points = num_points)
                pi_estimate = monte_carlo_pi_estimate(radius = rad_num, circle_area = area)
                actual_area = actual_circle_area(rad_num)
                log_estimate(num_points, pi_estimate)
                plot_pi_convergence()

        except:
            area = "Invalid input."
            pi_estimate = "o.O"
            actual_area = "beats me"

    return render_template('circle.html', area = area, pi_estimate = pi_estimate, actual_area = actual_area, pi = math.pi)

@app.route('/ellipse', methods=['GET', 'POST'])
def ellipse():
    area = actual_area = None

    if request.method == 'POST':
        try:
            num_points = int(request.form['num_points'])
            a = float(request.form['a'])
            b = float(request.form['b'])

            if num_points > 0 and a > 0 and b > 0:
                area = monte_carlo_ellipse_area(a=a, b=b, num_points=num_points)
                actual_area = math.pi * a * b
        except:
            area = "Invalid input."
            actual_area = "N/A"

    return render_template('ellipse.html', area=area, actual_area=actual_area)

@app.route('/reset-log')
def reset_log():
    log_file = 'static/pi_estimates.csv'
    if os.path.isfile(log_file):
        os.remove(log_file)
    convergence_plot = 'static/pi_convergence.png'
    if os.path.isfile(convergence_plot):
        os.remove(convergence_plot)
    return redirect(url_for('circle'))

@app.route('/sphere', methods=['GET', 'POST'])
def sphere():
    volume = actual_volume = None

    if request.method == 'POST':
        try:
            num_points = int(request.form['num_points'])
            rad_num = float(request.form['rad_num'])
            if num_points > 0:
                volume = monte_carlo_sphere_volume(radius=rad_num, num_points=num_points)
                actual_volume = actual_sphere_volume(radius=rad_num)
        except:
            volume = "Invalid input."
            actual_volume = "?"

    return render_template('sphere.html', volume=volume, actual_volume=actual_volume)

if __name__ == '__main__':
    app.run(debug = True)
