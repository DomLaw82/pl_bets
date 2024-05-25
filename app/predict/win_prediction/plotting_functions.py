import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import t, norm
import pandas as pd
import numpy as np

def plot_coefficients(models, outcome_labels):
    """Plots coefficients for each model."""

    plt.figure(figsize=(12, 6))

    for i, outcome in enumerate(outcome_labels):
        coefs = pd.DataFrame({
            'Feature': models[outcome].params.index,
            'Coefficient': models[outcome].params.values,
            'Outcome': outcome
        })
        plt.subplot(1, 3, i+1)
        sns.barplot(data=coefs, x='Coefficient', y='Feature', orient='h', color='skyblue')
        plt.title(f'Coefficients for {outcome.replace("_", " ").title()}')
        plt.axvline(x=0, color='black', linestyle='dashed', linewidth=1)
    plt.tight_layout()
    # plt.show()
    # plt.savefig('win_prediction/plots/model_coefficients_plot.png', dpi=300)

def plot_match_rating_distribution(data: pd.DataFrame, outcome_labels: list):
    """Plots the distribution of match ratings for each outcome."""

    plt.figure(figsize=(12, 6))
    
    for i, outcome in enumerate(outcome_labels):
        plt.subplot(1, 3, i + 1)
        sns.histplot(data=data, x='match_rating', hue=outcome, element='step', fill=True, common_norm=False, palette='muted', stat='density')
        plt.title(f'Match Rating Distribution for {outcome.replace("_", " ").title()}')

        zero_subset = data[data[outcome] == 0]
        one_subset = data[data[outcome] == 1]

        # Fit normal distribution to each subset
        mu_zero, std_zero = norm.fit(zero_subset['match_rating'])
        mu_one, std_one = norm.fit(one_subset['match_rating'])

        # Generate x values
        x_values_zero = np.linspace(zero_subset["match_rating"].min(), zero_subset["match_rating"].max(), 100)
        x_values_one = np.linspace(one_subset["match_rating"].min(), one_subset["match_rating"].max(), 100)

        # Calculate the PDF for each subset
        y_values_zero = norm.pdf(x_values_zero, mu_zero, std_zero)
        y_values_one = norm.pdf(x_values_one, mu_one, std_one)

        # Plot the PDF
        plt.plot(x_values_zero, y_values_zero, color='blue', label='Class 0 Fit')
        plt.plot(x_values_one, y_values_one, color='red', label='Class 1 Fit')
        
        plt.legend()

    plt.tight_layout()
    # plt.show()
    # plt.savefig('win_prediction/plots/match_rating_distribution_plot.png', dpi=300)

def plot_probability_by_match_rating(data: pd.DataFrame, models: dict, outcome_labels: list):
    """Plots the probability of each outcome by match rating."""
    plt.figure(figsize=(10, 6)) 

    markers = ['o', 'x', '+']
    colours = ['blue', 'orange', 'green']

    for outcome, marker, color in zip(outcome_labels, markers, colours):
        sns.regplot(x='match_rating', y=f"{outcome}_prob", data=data, logistic=True, label=outcome.replace("_", " ").title(), 
                    marker=marker, color=color, fit_reg=False, scatter_kws={'s': 50, 'alpha': 0.7})
        
        # Calculate and plot the logistic regression curve
        x_values = np.linspace(data['match_rating'].min(), data['match_rating'].max(), 100)
        y_values = models[outcome].predict(pd.DataFrame({'match_rating': x_values}))
        plt.plot(x_values, y_values, color=color)

    plt.title('Outcome Probabilities by Match Rating')
    plt.xlabel('Match Rating')
    plt.ylabel('Probability')
    plt.legend()
    # plt.show()
    # plt.savefig('win_prediction/plots/outcome_probability_by_match_rating_plot.png', dpi=300)