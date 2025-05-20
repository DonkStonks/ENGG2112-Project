import pandas as pd
import os

def data_set_cleaning():
    # ——— load raw CSV ———
    file_path = os.path.join(os.path.dirname(__file__),
                             '..', 'Crop_recommendation.csv')
    df = pd.read_csv(file_path)

    # ——— explicitly drop the two columns around GNDVI ———
    if 'GNDVI' in df.columns:
        # find its position
        idx = df.columns.get_loc('GNDVI')
        # build list: GNDVI plus next column if it exists
        to_drop = [df.columns[idx]]
        if idx + 1 < len(df.columns):
            to_drop.append(df.columns[idx + 1])
        df = df.drop(columns=to_drop)
        print(f"Dropped around GNDVI: {to_drop}")

    # ——— drop any other unwanted columns ———
    df = df.drop(columns=['field_id', 'date_of_image',
                          'Unnamed: 13', 'Unnamed: 14'],
                 errors='ignore')

    # ——— drop any residual 'Unnamed...' cols ———
    unnamed = [c for c in df.columns if c.startswith('Unnamed')]
    if unnamed:
        df = df.drop(columns=unnamed)
        print(f"Dropped dynamic Unnamed cols: {unnamed}")

    # ——— replace infinities & drop any rows with missing ———
    df = df.replace([float('inf'), float('-inf')], pd.NA).dropna()

    # ——— one-hot encode any categoricals ———
    cats = df.select_dtypes(include='object').columns.tolist()
    if cats:
        df = pd.get_dummies(df, columns=cats, drop_first=False)

    # ——— drop constant columns ———
    df = df.loc[:, df.nunique() > 1]

    # ——— compute the three agronomic indices ———
    df['Vegetation Growth Index']       = df['NDVI']     * df['temperature']
    df['Soil Moisture Vegetation Index'] = df['SAVI']     * df['soil_moisture']
    df['Water–Soil Balance Index']      = df['rainfall'] * df['soil_moisture']

    # ——— drop the raw columns now unused ———
    df = df.drop(columns=['NDVI', 'SAVI', 'soil_moisture'], errors='ignore')

    # ——— clean up all column names to Title Case ———
    def clean_col(name: str) -> str:
        return (name.strip()
                    .replace('_', ' ')
                    .replace('.', ' ')
                    .title())
    df = df.rename(columns=clean_col)

    return df

def main():
    print("Cleaning dataset…")
    data = data_set_cleaning()
    print(data.head())
    data.to_csv('./datasets/Crop_recommendation_cleaned.csv', index=False)

if __name__ == "__main__":
    main()
