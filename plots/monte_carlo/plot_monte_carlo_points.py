import numpy as np
from supplement.definitions import const
from mathematics.histogram import histogram
import plots.set_matplotlib
import matplotlib.pyplot as plt


r_increment = 0.01 # nm
r_border = 0.5 # nm
j_increment = 0.1 # MHz
j_border = 1 # MHz
a_increment = 1 # MHz
a_border = 10 # deg
threshold = 1.0e-10


def compute_distribution(points, weights, increment, border=0.0, scale=1.0):
    ''' Compute grid statistics ''' 
    points *= scale
    if points.size == 1 or all(v - points[0] < threshold for v in points):
        values = np.arange(points[0]-border, points[0]+border, increment)
    else:
        values = np.arange(np.amin(points)-border, np.amax(points)+border, increment)
    if weights != []:
        probabilities = histogram(points, bins=values, weights=weights)
    else:
        probabilities = histogram(points, bins=values)
    return values, probabilities


def plot_distribution(fig, x, y, axes_labels = ['Parameter (arb. u.)', 'Relative probability (arb. u.)']):
    ''' Plot an integration grid ''' 
    axes = fig.gca()
    axes.plot(x, y / np.amax(y), 'k-')
    axes.set_xlim(np.amin(x), np.amax(x))
    axes.set_xlabel(axes_labels[0])
    axes.set_ylabel(axes_labels[1])


def plot_monte_carlo_points(r_values, r_weights, xi_values, xi_weights, phi_values, phi_weights, alpha_values, alpha_weights, 
               beta_values, beta_weights, gamma_values, gamma_weights, j_values=[], j_weights=[]):   
    ''' Plot integration grids '''            
    fig = plt.figure(facecolor='w', edgecolor='w')
    # P(r)
    r_axis, r_prob = compute_distribution(r_values, r_weights, r_increment, border=r_border)
    plt.subplot(2, 4, 1)
    plot_distribution(fig, r_axis, r_prob, [r'$\mathit{r}$ (nm)', r'$\mathit{P(r)}$ (arb. u.)'])
    # P(xi)
    xi_axis, xi_prob = compute_distribution(xi_values, xi_weights, a_increment, border=a_border, scale=const['rad2deg'])
    plt.subplot(2, 4, 2)
    plot_distribution(fig, xi_axis, xi_prob, [r'$\mathit{\xi}$ $^\circ$', r'$\mathit{P(\xi)}$ (arb. u.)'])
    # P(phi)
    phi_axis, phi_prob = compute_distribution(phi_values, phi_weights, a_increment, border=a_border, scale=const['rad2deg'])
    plt.subplot(2, 4, 3)
    plot_distribution(fig, phi_axis, phi_prob, [r'$\mathit{\varphi}$ $^\circ$', r'$\mathit{P(\varphi)}$ (arb. u.)'])
    # P(alpha)
    alpha_axis, alpha_prob = compute_distribution(alpha_values, alpha_weights, a_increment, border=a_border, scale=const['rad2deg'])
    plt.subplot(2, 4, 4)
    plot_distribution(fig, alpha_axis, alpha_prob, [r'$\mathit{\alpha}$ $^\circ$', r'$\mathit{P(\alpha)}$ (arb. u.)'])
    # P(beta)
    beta_axis, beta_prob = compute_distribution(beta_values, beta_weights, a_increment, border=a_border, scale=const['rad2deg'])
    plt.subplot(2, 4, 5)
    plot_distribution(fig, beta_axis, beta_prob, [r'$\mathit{\beta}$ $^\circ$', r'$\mathit{P(\beta)}$ (arb. u.)'])
    # P(gamma)
    gamma_axis, gamma_prob = compute_distribution(gamma_values, gamma_weights, a_increment, border=a_border, scale=const['rad2deg'])
    plt.subplot(2, 4, 6)
    plot_distribution(fig, gamma_axis, gamma_prob, [r'$\mathit{\gamma}$ $^\circ$', r'$\mathit{P(\gamma)}$ (arb. u.)'])
    # P(J)
    if j_values != []:
        j_axis, j_prob = compute_distribution(j_values, j_weights, j_increment, border=j_border)
        plt.subplot(2, 4, 7)
        plot_distribution(fig, j_axis, j_prob, [r'$\mathit{J}$ (MHz)', r'$\mathit{P(J)}$ (arb. u.)'])
    plt.tight_layout()
    plt.draw()
    plt.pause(0.000001)