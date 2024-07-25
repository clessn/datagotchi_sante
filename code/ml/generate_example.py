import logging

from configs.deploy import DeployConfig as Config
from constants import Constants as C
from loaders import (
    load_attributes,
    load_codebook,
    load_feature_lookup_table,
    load_selected_features,
)
from tracking import write_example
from utils import configure_main_logger

logger = logging.getLogger(__name__)


# Create questionnaire
def create_questionnaire(
    df_feature_lookup,
    selected_features,
    df_codebook,
):
    questions = (
        df_feature_lookup.loc[
            df_feature_lookup[C.LOOKUP_FEATURE_NAME_COL].isin(selected_features),
            C.CODEBOOK_NAME_COL,
        ]
        .unique()
        .tolist()
    )

    df_questionnaire = df_codebook.loc[
        df_codebook[C.CODEBOOK_NAME_COL].isin(questions),
        [
            C.CODEBOOK_ID_COL,
            C.CODEBOOK_NAME_COL,
            C.CODEBOOK_QUESTION_COL,
            C.CODEBOOK_CHOICE_COL,
        ],
    ]
    return df_questionnaire


def create_example(df_attributes, raw_variable_names):
    df_users = df_attributes.sample(n=Config.N_USERS, random_state=42)[
        raw_variable_names
    ]
    return df_users


# Run crossval
if __name__ == "__main__":
    logger = configure_main_logger("generate_example")
    ml_run_path = C.ML_PATH / eval(f"C.{Config.RUN_TYPE}")
    frozen_library_folder_name = Config.FEATURE_LIBRARY_VERSION

    # Load codebook
    df_codebook = load_codebook(C.CODEBOOK_PATH, Config.CODEBOOK_VERSION)

    # Load feature lookup-table
    df_feature_lookup = load_feature_lookup_table(
        ml_run_path / C.FEATURE_LIBRARIES_FOLDER_NAME / frozen_library_folder_name,
        C.FEATURE_LOOKUP_FILENAME,
    )

    # Load selected feature
    selected_features = load_selected_features(
        Config.FEATURE_SELECTION_METHOD,
        ml_run_path / C.FEATURE_SELECTION_FOLDER_NAME / frozen_library_folder_name,
        C.FEATURE_SELECTION_FILENAME,
    )

    # Create questionnaire
    df_questionnaire = create_questionnaire(
        df_feature_lookup,
        selected_features,
        df_codebook,
    )

    # Create example
    df_attributes = load_attributes(ml_run_path, C.ATTRIBUTES_FILENAME)
    df_example = create_example(
        df_attributes, df_questionnaire[C.CODEBOOK_NAME_COL].tolist()
    )

    write_example(
        df_questionnaire,
        df_example,
        ml_run_path / C.DEPLOY_FOLDER_NAME,
        C.QUESTIONNAIRE_FILENAME,
        C.EXAMPLE_FILENAME,
    )
