import pandas as pd
import numpy as np
import sys

def topsis(input_file, weights, impacts, output_file):
    # Read input data with a specified encoding
    try:
        df = pd.read_csv(input_file, encoding='ISO-8859-1')  # Try 'ISO-8859-1' or other encodings
    except UnicodeDecodeError:
        print("Error reading the CSV file. Please check the file's encoding.")
        sys.exit(1)

    # Ensure valid structure
    if df.shape[1] < 3:
        raise ValueError("The input file must have at least three columns (Identifier and Criteria).")

    # Extract decision matrix and identifiers
    decision_matrix = df.iloc[:, 1:].values  # Exclude the first column (Identifier)
    identifiers = df.iloc[:, 0].values  # First column (Identifier)

    # Parse weights and impacts
    weights = list(map(float, weights.split(',')))
    impacts = impacts.split(',')

    # Validate dimensions
    if len(weights) != decision_matrix.shape[1] or len(impacts) != decision_matrix.shape[1]:
        raise ValueError("The number of weights and impacts must match the number of criteria.")

    # Normalize decision matrix
    norm_matrix = decision_matrix / np.sqrt((decision_matrix ** 2).sum(axis=0))

    # Apply weights
    weighted_matrix = norm_matrix * weights

    # Determine ideal best and worst values
    ideal_best = [max(weighted_matrix[:, i]) if impacts[i] == '+' else min(weighted_matrix[:, i]) for i in range(len(impacts))]
    ideal_worst = [min(weighted_matrix[:, i]) if impacts[i] == '+' else max(weighted_matrix[:, i]) for i in range(len(impacts))]

    # Calculate distances from ideal values
    dist_to_best = np.sqrt(((weighted_matrix - ideal_best) ** 2).sum(axis=1))
    dist_to_worst = np.sqrt(((weighted_matrix - ideal_worst) ** 2).sum(axis=1))

    # Calculate relative closeness to the ideal solution
    performance_scores = dist_to_worst / (dist_to_best + dist_to_worst)

    # Append scores and ranks to the original data
    df['Performance Score'] = performance_scores
    df['Rank'] = df['Performance Score'].rank(ascending=False)

    # Save results to the specified output file
    df.to_csv(output_file, index=False)
    print(f"Results successfully saved to {output_file}")

# Script entry point for standalone execution
if __name__ == "__main__":
    # Modify these parameters for execution
    input_file = "102203622-data.csv"  # Your input file name
    weights = "1,1,1,1,1"  # Provide weights (one for each criterion)
    impacts = "+,+,+,+,+"  # Specify impacts for each criterion
    output_file = "102203622-result.csv"  # Desired output file name

    # Call the TOPSIS function
    topsis(input_file, weights, impacts, output_file)
