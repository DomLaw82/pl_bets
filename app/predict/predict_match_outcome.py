# Description: Predict the outcome of a match based on the trained model

# Input: Home team, away team, unavailable players (home and away)
# Output: Predicted match stats (goals, shots, shots on target, corners, fouls, yellow cards, red cards)

# Remove injured/unavailable players from consideration
# Use dataset_creation.create_dataset modules to create a dataset for both teams involved in the game, minus injured/unavailable players
# Read in the model: stats_regression_model.h5
# Use the model to predict the match stats for the game
# Return these stats to the user