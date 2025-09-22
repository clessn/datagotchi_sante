from sklearn.metrics import r2_score

from app.ml.constants import Constants as C
from app.ml.loaders import load_results_predictions

def compute_r2():

    # select path
    ml_run_path = C.ML_PATH / "real"
    experiments_path = ml_run_path / C.EXPERIMENTS_FOLDER_NAME
    selected_experiment = "11_export_question_with_filter_on_countries"
    selected_artifacts = "KindheartedLeopard2633"
    artifacts_path = (
        experiments_path / selected_experiment / C.EXPERIMENTS_ARTIFACTS_FOLDER_NAME / selected_artifacts
    )
    
    # Load predictions results
    predictions_df = load_results_predictions(
            artifacts_path, C.PREDICTIONS_FILENAME
        )

    # Compute R² for each model and fold
    for model in predictions_df["model_name"].unique():
        print(f"Model: {model}")
        model_df = predictions_df[predictions_df["model_name"] == model]
        for fold in model_df["fold_id"].unique():
            fold_df = model_df[model_df["fold_id"] == fold]
            fold_df = fold_df.dropna(subset=["y_test", "y_predict"])
            r2 = r2_score(fold_df["y_test"], fold_df["y_predict"])
            print(f"  Fold {fold}: R² = {r2:.4f}")
