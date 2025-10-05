import pandas as pd
import numpy as np

def predict_dataframe(X: pd.DataFrame):
    """
    Mock prediction function for exoplanet classification.
    
    This function simulates a model prediction based on the Signal-to-Noise Ratio (snr).
    A high SNR suggests a stronger transit signal, making it more likely to be a planet.

    Args:
        X (pd.DataFrame): DataFrame containing the features. Must include 'snr'.

    Returns:
        tuple: (predictions: np.array, probabilities: np.array)
               Predictions are 1 (Planet) or 0 (Non-Planet).
               Probabilities are the confidence scores (0.0 to 1.0).
    """
    if 'snr' not in X.columns:
        print("Warning: 'snr' column missing. Returning default non-planet predictions.")
        return np.zeros(len(X), dtype=int), np.zeros(len(X)) + 0.5

    # Simple mock logic: If SNR is high (> 100), classify as a Planet (1).
    # Otherwise, classify as a Non-Planet (0).
    predictions = (X['snr'] > 100).astype(int).values
    
    # Generate probabilities: 
    # High SNR gives high probability of being 1 (Planet)
    # Low SNR gives high probability of being 0 (Non-Planet, i.e., 1 - probability of 1)
    
    # Scale SNR for a pseudo-probability: Max SNR assumed around 1000 for scaling
    max_snr = 1000.0
    scaled_snr = np.clip(X['snr'] / max_snr, 0.0, 1.0)
    
    # Probabilities are higher for the predicted class
    probabilities = np.where(
        predictions == 1, 
        0.5 + (scaled_snr / 2),  # If prediction is 1, prob is in [0.5, 1.0]
        0.5 - (scaled_snr / 2)   # If prediction is 0, prob is in [0.0, 0.5]
    )
    
    # Ensure probabilities are clipped to valid range (shouldn't be needed, but safe)
    probabilities = np.clip(probabilities, 0.01, 0.99)
    
    return predictions, probabilities

if __name__ == '__main__':
    # Example usage for testing
    data = {
        'orbital_period': [1.0, 50.0, 10.0],
        'transit_duration': [2.0, 0.5, 1.5],
        'planet_radius': [1.0, 5.0, 3.0],
        'transit_depth': [100.0, 500.0, 50.0],
        'snr': [50.0, 250.0, 120.0]  # Key determinant in mock logic
    }
    test_df = pd.DataFrame(data)
    
    preds, probs = predict_dataframe(test_df)
    test_df['Prediction'] = preds
    test_df['Probability'] = probs
    
    print("--- Test Predictions ---")
    print(test_df)

    # Expected: 
    # Row 0 (SNR 50) -> Prediction 0, Prob ~ 0.475
    # Row 1 (SNR 250) -> Prediction 1, Prob ~ 0.625
    # Row 2 (SNR 120) -> Prediction 1, Prob ~ 0.56
