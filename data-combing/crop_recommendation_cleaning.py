import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def data_set_cleaning():
    # Adjust the path to point to the dataset (one folder up)
    file_path = os.path.join(os.path.dirname(__file__), '..', 'Crop_recommendation.csv')

    # Load dataset
    df = pd.read_csv(file_path)

    # Remove unnecessary columns
    df = df.drop(['field_id','date_of_image','Unnamed: 13','Unnamed: 14'],axis=1)

    # Drop completely empty or unnamed columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    # Replace inf/-inf with NaN and drop rows with any missing values
    df.replace([float('inf'), float('-inf')], pd.NA, inplace=True)
    df.dropna(inplace=True)

    # One-hot encode categorical columns if present (keep all categories)
    categorical_cols = df.select_dtypes(include=['object']).columns
    if not categorical_cols.empty:
        df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=False)
    else:
        df_encoded = df.copy()

    # Drop constant columns (same value everywhere)
    df_encoded = df_encoded.loc[:, df_encoded.nunique() > 1]


    #Calculate NDVI and SAVI
    df_encoded["NDVI_temp"] = df_encoded["NDVI"] * df_encoded["temperature"]
    df_encoded["NDVI_rainfall"] = df_encoded["NDVI"] * df_encoded["rainfall"]
    df_encoded["SAVI_soil_moisture"] = df_encoded["SAVI"] * df_encoded["soil_moisture"]

    return df_encoded


def main():
    print("Cleaning dataset...")
    data = data_set_cleaning()
    print(data.head())
    data.to_csv('./datasets/Crop_recommendation_cleaned.csv', index=False)


if __name__ == "__main__":
    main()


