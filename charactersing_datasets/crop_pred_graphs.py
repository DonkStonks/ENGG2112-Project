import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def plot_cleaned_heatmap():
    # Adjust the path to point to the dataset (one folder up)
    file_path = os.path.join(os.path.dirname(__file__), '..', 'crop_yield_dataset.csv')

    # Load dataset
    df = pd.read_csv(file_path)

    # Replace inf/-inf with NaN and drop rows with any missing values
    df.replace([float('inf'), float('-inf')], pd.NA, inplace=True)
    df.dropna(inplace=True)

    # One-hot encode categorical columns if present
    categorical_cols = df.select_dtypes(include=['object']).columns
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # Drop constant columns (same value everywhere)
    df_encoded = df_encoded.loc[:, df_encoded.nunique() > 1]

    # Select only numeric columns
    numeric_df = df_encoded.select_dtypes(include=['number'])

    if numeric_df.empty:
        print("No usable numeric columns found after cleaning and encoding.")
        return

    # Compute correlation matrix
    corr_matrix = numeric_df.corr()

    # Plot heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
    plt.title('Feature Correlation Heatmap (Crop Yield Dataset)')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_cleaned_heatmap()
