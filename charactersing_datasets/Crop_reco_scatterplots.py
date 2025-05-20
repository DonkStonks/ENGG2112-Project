import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_yield_vs_features(csv_path, out_dir='output_plots'):
    # create output directory if needed
    os.makedirs(out_dir, exist_ok=True)
    
    # load data
    df = pd.read_csv(csv_path)
    
    # identify numeric columns, excluding the target
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    features = [c for c in numeric_cols if c.lower() != 'yield']
    
    # loop and plot
    for feat in features:
        plt.figure(figsize=(6, 4))
        plt.scatter(df[feat], df['Yield'], alpha=0.6)
        plt.xlabel(feat)
        plt.ylabel('Yield')
        plt.title(f'Yield vs {feat}')
        plt.tight_layout()
        
        # save and close
        filename = f'yield_vs_{feat.replace(" ", "_").lower()}.png'
        plt.savefig(os.path.join(out_dir, filename), dpi=150)
        plt.close()

if __name__ == '__main__':
    # adjust path if necessary
    plot_yield_vs_features(
        csv_path='./datasets/Crop_recommendation_cleaned.csv',
        out_dir='./plots'
    )
    print("All scatterplots saved to ./plots/")
