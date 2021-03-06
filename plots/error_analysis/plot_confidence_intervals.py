import sys
import numpy as np
import plots.set_matplotlib
from plots.set_matplotlib import best_rcparams
import matplotlib.pyplot as plt
from plots.best_layout import best_layout 
import warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")
from supplement.definitions import const    


def plot_confidence_interval(axes, parameter_values, score_values, optimized_parameter_value, parameter_id, score_threshold, numerical_error):
    # Set the color ranges
    cmin = np.amin(score_values) + score_threshold
    cmax = 2 * cmin
    # Plot the score vs fitting parameter
    axes.scatter(parameter_values, score_values, c=score_values, cmap='jet_r', vmin=cmin, vmax=cmax)
    xlabel_text = const['fitting_parameters_labels'][parameter_id.name][0] + r'$_{%d, %d}$' % (parameter_id.spin_pair+1, parameter_id.component+1) + ' ' + const['fitting_parameters_labels'][parameter_id.name][1]
    ylabel_text = r'$\mathit{\chi^2}$'
    axes.set_xlabel(xlabel_text)
    axes.set_ylabel(ylabel_text)
    # Depict the confidence interval
    best_score = np.amin(score_values)
    indices_confidence_interval = np.where(score_values - best_score <= score_threshold)[0]
    confidence_interval_lower_bound = parameter_values[indices_confidence_interval[0]]
    confidence_interval_upper_bound = parameter_values[indices_confidence_interval[-1]]
    axes.axvspan(confidence_interval_lower_bound, confidence_interval_upper_bound, facecolor="lightgray", alpha=0.3, label="confidence interval")
    # Depict the optimized fitting parameter
    index_optimized_parameter = min(range(len(parameter_values)), key=lambda i: abs(parameter_values[i]-optimized_parameter_value))
    minimal_score = score_values[index_optimized_parameter]
    axes.plot(optimized_parameter_value, minimal_score, color='black', marker='o', markerfacecolor='white', clip_on=False, label = "fitting result")
    # Depict the score thresholds
    threshold1 = (best_score + score_threshold - numerical_error) * np.ones(parameter_values.size)
    threshold2 = (best_score + score_threshold) * np.ones(parameter_values.size)
    axes.plot(parameter_values, threshold1, 'm--', label = r'$\mathit{\chi^{2}_{min}}$ + $\mathit{\Delta\chi^{2}_{ci}}$')
    axes.plot(parameter_values, threshold2, 'k--', label = r'$\mathit{\chi^{2}_{min}}$ + $\mathit{\Delta\chi^{2}_{ci}}$ + $\mathit{\Delta\chi^{2}_{ne}}$')
    axes.ticklabel_format(axis='y', style='sci', scilimits=(0,0), useMathText=True) 
    # Make axes square
    xl, xh = axes.get_xlim()
    yl, yh = axes.get_ylim()
    axes.set_aspect((xh-xl)/(yh-yl))


def plot_confidence_intervals(score_vs_parameters, error_analysis_parameters, fitting_parameters, optimized_parameters, score_threshold, numerical_error):
    ''' Plots chi2 as a function of individual fitting parameters '''
    figsize = [10, 8]
    num_subplots = sum(len(i) for i in error_analysis_parameters)
    best_rcparams(num_subplots)
    layout = best_layout(figsize[0], figsize[1], num_subplots)
    fig = plt.figure(figsize=(figsize[0], figsize[1]), facecolor='w', edgecolor='w')
    c = 0
    for i in range(len(error_analysis_parameters)):
        for j in range(len(error_analysis_parameters[i])):
            parameter_id = error_analysis_parameters[i][j]
            score_vs_parameter = score_vs_parameters[c]
            parameter_values = score_vs_parameter['parameter']  / const['fitting_parameters_scales'][parameter_id.name]
            score_values = score_vs_parameter['score']
            parameter_index = parameter_id.get_index(fitting_parameters['indices']) 
            optimized_parameter_value = optimized_parameters[parameter_index] / const['fitting_parameters_scales'][parameter_id.name]
            if num_subplots == 1:
                axes = fig.gca()
            else:
                axes = fig.add_subplot(layout[0], layout[1], c+1)
            plot_confidence_interval(axes, parameter_values, score_values, optimized_parameter_value, parameter_id, score_threshold, numerical_error)
            c += 1
    left = 0
    right = float(layout[1])/float(layout[1]+1)
    bottom = 0.5 * (1-right)
    top = 1 - bottom
    fig.tight_layout(rect=[left, bottom, right, top])
    handles, labels = fig.axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc='center left', bbox_to_anchor=(right+0.01, 0.5), frameon=False) 
    plt.draw()
    plt.pause(0.000001)
    return fig