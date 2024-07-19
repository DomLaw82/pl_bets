import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import t, norm, linregress
import pandas as pd
import numpy as np
    
def plot_log_reg_coefficients(models, outcome_labels):
    importances_data = []

    for outcome in outcome_labels:
        importances = models[outcome].coef_[0]
        feature_names = models[outcome].feature_names_in_

        for feature_name, importance in list(zip(feature_names, importances)):
            importances_data.append({
                'Outcome': outcome.replace('_', ' ').title(),
                'Feature': feature_name,
                'Importance': importance
            })

    df_importances = pd.DataFrame(importances_data)

    plt.figure(figsize=(14, 8))
    sns.barplot(x='Feature', y='Importance', hue='Outcome', data=df_importances)
    plt.title('Feature Importances by Outcome')
    plt.xticks(rotation=90)
    plt.tight_layout()
    # plt.show()
    plt.savefig('win_prediction_modules/plots/model_coefficients_plot.png')

def plot_feature_distribution(data: pd.DataFrame, outcome_labels: list, feature: str):
    """Plots the distribution of match ratings for each outcome."""

    plt.figure(figsize=(12, 6))
    
    for i, outcome in enumerate(outcome_labels):
        plt.subplot(1, 3, i + 1)
        sns.histplot(data=data, x=feature, hue=outcome, element='step', fill=True, common_norm=False, palette='muted', stat='density')
        plt.title(f'{feature} for {outcome.replace("_", " ").title()}')

        zero_subset = data[data[outcome] == 0]
        one_subset = data[data[outcome] == 1]

        # Fit normal distribution to each subset
        mu_zero, std_zero = norm.fit(zero_subset[feature])
        mu_one, std_one = norm.fit(one_subset[feature])

        # Generate x values
        x_values_zero = np.linspace(zero_subset[feature].min(), zero_subset[feature].max(), 100)
        x_values_one = np.linspace(one_subset[feature].min(), one_subset[feature].max(), 100)

        # Calculate the PDF for each subset
        y_values_zero = norm.pdf(x_values_zero, mu_zero, std_zero)
        y_values_one = norm.pdf(x_values_one, mu_one, std_one)

        # Plot the PDF
        plt.plot(x_values_zero, y_values_zero, color='blue', label='Class 0 Fit')
        plt.plot(x_values_one, y_values_one, color='red', label='Class 1 Fit')
        
        plt.legend()

    plt.tight_layout()
    # plt.show()
    plt.savefig(f'win_prediction_modules/plots/{feature}_distribution_plot.png', dpi=300)

def plot_probability_by_feature(data: pd.DataFrame, outcome_labels: list, feature: str):
    """Plots the probability of each outcome by a specified feature."""
    plt.figure(figsize=(10, 6)) 

    markers = ['o', 'x', '+']
    colours = ['blue', 'orange', 'green']

    for outcome, marker, color in zip(outcome_labels, markers, colours):
        # sns.regplot(x='match_rating', y=f"{outcome}_prob", data=data, logistic=True, label=outcome.replace("_", " ").title(), 
        #         marker=marker, color=color, scatter_kws={'s': 50, 'alpha': 0.7})
        sns.scatterplot(x=feature, y=f"{outcome}_prob", data=data, label=outcome.replace("_", " ").title(), 
                        marker=marker, color=color)
        x = data[feature]
        y = data[f"{outcome}_prob"]

        slope, intercept, r_value, p_value, std_err = linregress(x, y)
        plt.plot(x, intercept + slope * x, color=color, linestyle='--')

    plt.title(f'Outcome Probabilities by {feature}')
    plt.xlabel(feature)
    plt.ylabel('Probability')
    plt.legend()
    # plt.show()
    plt.savefig(f'win_prediction_modules/plots/outcome_probability_by_{feature}_plot.png', dpi=300)