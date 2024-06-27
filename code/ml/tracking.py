import json
import logging
import os
import random
from datetime import datetime
from pathlib import Path

import pandas as pd
from config import Config
from constants import Constants as C
from loaders import load_results_metrics

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


def write_feature_library(df_features, df_targets):
    # TODO: use parquet instead
    df_features.to_csv(C.FEATURE_LIBRARIES_PATH / C.FEATURE_LIBRARY_FILENAME)
    df_targets.to_csv(C.FEATURE_LIBRARIES_PATH / C.TARGETS_FILENAME)
    logger.info("Feature library saved with targets")


def write_selected_features(
    feature_names, feature_scores, feature_selected, method_name
):

    # Create a dictionary with the data
    data = {
        "feature_names": feature_names,
        "feature_scores": feature_scores,
        "feature_selected": feature_selected,
    }

    # Create DataFrame
    df = pd.DataFrame(data)
    df.to_csv(
        C.FEATURE_SELECTION_PATH / C.FEATURE_SELECTION_FILENAME.format(method_name),
        index=False,
    )

    logger.info("Selected features stored with sucess")


def track_results(metrics_df, predictions_df):

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

    if os.path.isfile(C.EXPERIMENTS_VERSION_PATH / C.METRICS_FILENAME):
        metrics_df_old = load_results_metrics()
        metrics_df = pd.concat((metrics_df_old, metrics_df), ignore_index=True)
        logger.info("Updating metrics dashboard...")
    metrics_df.to_csv(C.EXPERIMENTS_VERSION_PATH / C.METRICS_FILENAME, index=False)
    logger.info("Metrics file saved")

    # write artifacts
    artifacts_run_id_path = C.EXPERIMENTS_VERSION_ARTIFACTS_PATH / run_id
    assert not os.path.isdir(artifacts_run_id_path)
    Path(artifacts_run_id_path).mkdir(parents=True, exist_ok=True)

    # - write config
    config_dict = Config.to_dict()
    with open(artifacts_run_id_path / C.ARTIFACTS_CONFIG_FILENAME, "w") as json_file:
        json.dump(config_dict, json_file, indent=4)
    logger.info("Config artifacts saved")

    # - write predictions
    predictions_df.to_csv(artifacts_run_id_path / C.ARTIFACTS_PREDICTIONS_FILENAME)
    logger.info("Predictions saved")
