import json
import logging
import os
import random
from datetime import datetime
from pathlib import Path

import pandas as pd
from constants import Constants as C
from loaders import load_results_metrics
from utils import create_label

logger = logging.getLogger(__name__)

adjectives = [
    "Brave",
    "Calm",
    "Delightful",
    "Eager",
    "Fancy",
    "Gentle",
    "Happy",
    "Jolly",
    "Kind",
    "Lively",
    "Nice",
    "Polite",
    "Quick",
    "Silly",
    "Thankful",
    "Wise",
    "Zany",
    "Bright",
    "Cheerful",
    "Witty",
    "Clever",
    "Friendly",
    "Graceful",
    "Humorous",
    "Joyful",
    "Loyal",
    "Playful",
    "Sincere",
    "Vibrant",
    "Charming",
    "Determined",
    "Energetic",
    "Fearless",
    "Generous",
    "Helpful",
    "Inventive",
    "Kindhearted",
]

nouns = [
    "Lion",
    "Tiger",
    "Bear",
    "Eagle",
    "Shark",
    "Dolphin",
    "Panda",
    "Koala",
    "Fox",
    "Wolf",
    "Falcon",
    "Hawk",
    "Leopard",
    "Cheetah",
    "Giraffe",
    "Elephant",
    "Zebra",
    "Rabbit",
    "Owl",
    "Turtle",
    "Parrot",
    "Whale",
    "Penguin",
    "Lynx",
    "Hedgehog",
    "Squirrel",
    "Badger",
    "Otter",
    "Raccoon",
    "Porcupine",
    "Bison",
    "Buffalo",
    "Moose",
    "Reindeer",
    "Skunk",
    "Vulture",
    "Peacock",
    "Frog",
    "Crocodile",
    "Alligator",
]


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        # If the object has a __dict__ attribute, use it for serialization
        if hasattr(obj, "__dict__"):
            return str(obj)
        return obj


def write_feature_library(
    df_features,
    df_targets,
    df_feature_lookup,
    path,
    feature_filename,
    targets_filename,
    feature_lookup_filename,
):
    # TODO: use parquet instead
    # Create directory if missing
    Path(path).mkdir(parents=True, exist_ok=True)

    # Write features and targets
    df_features.to_csv(path / feature_filename)
    df_targets.to_csv(path / targets_filename)
    df_feature_lookup.to_csv(path / feature_lookup_filename, index=False)
    logger.info("Feature library saved with targets")


def write_selected_features(
    feature_names,
    feature_scores,
    feature_selected,
    feature_selection_method,
    path,
    filename,
):

    # Create directory if missing
    Path(path).mkdir(parents=True, exist_ok=True)

    # Create label from method dictionary
    method_name, method_params = feature_selection_method
    feature_selection_method_label = create_label(method_name, method_params)

    # Create a dictionary with the data
    data = {
        "feature_names": feature_names,
        "feature_scores": feature_scores,
        "feature_selected": feature_selected,
    }

    # Create DataFrame
    df = pd.DataFrame(data)
    df.to_csv(path / filename.format(feature_selection_method_label), index=False)

    logger.info("Selected features stored with sucess")


def track_results(
    metrics_df,
    predictions_df,
    best_hyperparameters,
    Config,
    metrics_path,
    artifacts_path,
    metrics_filename,
    artifacts_config_filename,
    artifacts_hyperparameter_filename,
    artifacts_predictions_filename,
):

    logger.debug("Writing metrics file....")

    # Create directory if missing
    Path(metrics_path).mkdir(parents=True, exist_ok=True)
    Path(artifacts_path).mkdir(parents=True, exist_ok=True)

    # create a run_id and timestamp
    adjective = random.choice(adjectives)
    noun = random.choice(nouns)
    run_id = f"{adjective}{noun}{random.randint(1, 10000)}"
    now = datetime.now()
    date_time_str = now.strftime("%Y-%m-%d %H:%M")

    # add id and timestamp in metrics
    metrics_df.insert(
        0, C.METRICS_TIMESTAMP_FIELD, [date_time_str] * metrics_df.shape[0]
    )
    metrics_df.insert(0, C.METRICS_RUN_ID_FIELD, [run_id] * metrics_df.shape[0])

    if os.path.isfile(metrics_path / metrics_filename):
        metrics_df_old = load_results_metrics(metrics_path, metrics_filename)
        metrics_df = pd.concat((metrics_df_old, metrics_df), ignore_index=True)
        logger.info("Updating metrics dashboard...")
    metrics_df.to_csv(metrics_path / metrics_filename, index=False)
    logger.info("Metrics file saved")

    # write artifacts
    artifacts_run_id_path = artifacts_path / run_id
    assert not os.path.isdir(artifacts_run_id_path)
    Path(artifacts_run_id_path).mkdir(parents=True, exist_ok=True)

    # - write config
    config_dict = Config.to_dict()
    with open(artifacts_run_id_path / artifacts_config_filename, "w") as json_file:
        json.dump(config_dict, json_file, indent=4)
    logger.info("Config artifacts saved")

    # - write hyperparameters
    with open(
        artifacts_run_id_path / artifacts_hyperparameter_filename, "w"
    ) as json_file:
        json.dump(best_hyperparameters, json_file, indent=4, cls=CustomEncoder)
    logger.info("Best hyperparameters artifacts saved")

    # - write predictions
    predictions_df.to_csv(artifacts_run_id_path / artifacts_predictions_filename)
    logger.info("Predictions saved")


def write_example(
    df_questionnaire, df_example, deploy_path, questionnaire_filename, example_filename
):
    # Create directory if missing
    Path(deploy_path).mkdir(parents=True, exist_ok=True)

    df_questionnaire.to_csv(deploy_path / questionnaire_filename, index=False)
    df_example.to_csv(deploy_path / example_filename)
    logger.info("Questionnaire and example saved")
