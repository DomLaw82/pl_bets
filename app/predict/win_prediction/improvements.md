Interaction Terms: You might want to explore interaction effects between features (e.g., how home advantage interacts with team form).
Model Selection: While logistic regression is a good starting point, consider trying other models like random forests or gradient boosting for potentially better results.
Overfitting: Be cautious of overfitting, especially with complex models. Use techniques like cross-validation and regularization.
Data Quality: Ensure that your head-to-head data is accurate and complete.
Home Advantage: In your dataset, you don't need a home_advantage column as the gd_form_home and gd_form_away features already capture home advantage.

gd_form_home and _away to use the sum of the goal differences for the previous 6 games instead of the mean
Calculate short, medium and long term form, e.g. last 3, 5, 10 games
Weighted form windows