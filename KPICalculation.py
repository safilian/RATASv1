import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from scipy.stats import pearsonr
import pandas as pd
import pingouin as pg

def evaluate_model_kpis(file_path, actual_col, predicted_col, wordcount_col='word_count'):
    """
    Reads an Excel file and computes MAE, RMSE, R², and Pearson's r for:
     1) All data
     2) Category A: word_count < 600
     3) Category B: word_count >= 600

    Parameters:
    -----------
    file_path : str
        Path to the Excel file.
    actual_col : str
        Column name for actual scores.
    predicted_col : str
        Column name for predicted scores.
    wordcount_col : str
        Column name for word count (default is 'word_count').
    """

    # ---------------------------
    # 1. Read Excel File
    # ---------------------------
    df = pd.read_excel(file_path, engine='openpyxl')

    # ---------------------------
    # 2. Check Column Existence
    # ---------------------------
    for col in [actual_col, predicted_col, wordcount_col]:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' not found in the Excel file.")

    # ---------------------------
    # 3. Helper Function to Compute KPIs
    # ---------------------------
    def compute_kpis(y_actual, y_predicted):
        # Convert to float (in case they're not)
        y_actual = y_actual.astype(float)
        y_predicted = y_predicted.astype(float)

        mae_val = mean_absolute_error(y_actual, y_predicted)
        rmse_val = np.sqrt(mean_squared_error(y_actual, y_predicted))
        r2_val = r2_score(y_actual, y_predicted)
        pearson_r_val, _ = pearsonr(y_actual, y_predicted)

        return mae_val, rmse_val, r2_val, pearson_r_val

    # ---------------------------
    # 4. Overall Data
    # ---------------------------
    y_actual_all = df[actual_col]
    y_pred_all = df[predicted_col]
    mae_all, rmse_all, r2_all, r_all = compute_kpis(y_actual_all, y_pred_all)

    # ---------------------------
    # 5. Category A Data (word_count < 600)
    # ---------------------------
    df_A = df[df[wordcount_col] < 600]
    y_actual_A = df_A[actual_col]
    y_pred_A = df_A[predicted_col]
    mae_A, rmse_A, r2_A, r_A = compute_kpis(y_actual_A, y_pred_A) if len(df_A) > 0 else (None, None, None, None)

    # ---------------------------
    # 6. Category B Data (word_count >= 600)
    # ---------------------------
    df_B = df[df[wordcount_col] >= 600]
    y_actual_B = df_B[actual_col]
    y_pred_B = df_B[predicted_col]
    mae_B, rmse_B, r2_B, r_B = compute_kpis(y_actual_B, y_pred_B) if len(df_B) > 0 else (None, None, None, None)

    # ---------------------------
    # 7. Print Results
    # ---------------------------
    def print_kpis(title, mae_val, rmse_val, r2_val, pearson_val):
        print(f"\n=== {title} ===")
        if mae_val is None:
            print("No data available for this category.")
            return
        print(f"MAE: {mae_val:.4f}")
        print(f"RMSE: {rmse_val:.4f}")
        print(f"R²: {r2_val:.4f}")
        print(f"Pearson's r: {pearson_val:.4f}")

    # Print Overall
    print_kpis("Overall Data", mae_all, rmse_all, r2_all, r_all)
    # Print Category A
    print_kpis("Category A (word_count < 600)", mae_A, rmse_A, r2_A, r_A)
    # Print Category B
    print_kpis("Category B (word_count >= 600)", mae_B, rmse_B, r2_B, r_B)


# ---------------------------
#Example Usage






def compute_icc_from_excel(file_path, col1, col2, col3):
    """
    Computes the Intraclass Correlation Coefficient (ICC) to evaluate scoring reliability.

    Parameters:
    - file_path (str): Path to the Excel file.
    - col1, col2, col3 (str): Column names representing three different runs.

    Returns:
    - float: ICC value
    """
    # Load the Excel file
    df = pd.read_excel(file_path)

    # Extract the relevant columns
    scores = df[[col1, col2, col3]]

    # Convert DataFrame to long format for ICC computation
    melted = scores.melt(var_name="Run", value_name="Score")
    melted["Subject"] = melted.index % len(df)  # Assign a unique subject ID for ICC calculation

    # Compute ICC (Two-way mixed, single measures)
    icc_results = pg.intraclass_corr(data=melted, targets="Subject", raters="Run", ratings="Score")
    icc_value = icc_results.loc[icc_results['Type'] == 'ICC3', 'ICC'].values[0]

    return icc_value




if __name__ == "__main__":
    file_path = r"C:\Users\MSD\Desktop\my_project\Matching_Scoring\updated_scores.xlsx"      # Change to your Excel file path
    actual_column = "new_x6"                # Change to your actual scores column
    predicted_column = "RATAS"          # Change to your predicted scores column
    wordcount_column = "word_count"               # Ensure this matches your file
    evaluate_model_kpis(file_path, actual_column, predicted_column, wordcount_col=wordcount_column)


# Example usage
# file_path = r"C:\Users\MSD\Desktop\my_project\Matching_Scoring\updated_scores.xlsx"
# icc_score = compute_icc_from_excel(file_path, "new_x1", "new_x3", "new_x2")
# print(f"ICC Score: {icc_score:.4f}")
