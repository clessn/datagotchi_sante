import os
from pathlib import Path
import re

import pandas as pd
from dotenv import load_dotenv
import pypandoc

from app.ml.constants import Constants as C

# Load the .env file
load_dotenv()



def extract_url(text):
    """Return first URL found in a text, or None."""
    if not isinstance(text, str):
        return None
    match = re.search(r"(https?://[^\s]+)", text)
    return match.group(1) if match else None


# ============================================================
#                STUDY 1 — CLEANING FUNCTION
# ============================================================

def clean_study1_codebook():
    # --- Starred question IDs ---
    STARRED_IDS = {
        "travail_domaine_1", "origines_ethniques", "married", "car_model", "smoking",
        "act_friends", "act_volunteer", "act_nature_1", "style", "maladies_1",
        "autogestion_9", "sommeil_1", "chronotype", "LatDec_3", "SoutSup_6",
        "quartier_domicile_3", "quartier_opportunite", "consult_who_1",
        "nb_friends_dispo", "issue_ai_data_3"
    }

    # --- Load ---
    original_df = pd.read_csv(C.CODEBOOK_PATH / "frozen_codebook_october_15.csv")

    # Load source mapping
    sources_df = pd.read_csv("codebook_study1_sources.csv")
    sources_map = dict(zip(sources_df["question_id"], sources_df["source"]))

    # Extract all CSM_QA* rows BEFORE filtering
    csm_df = original_df[
        original_df["raw_variable_name"].astype(str).str.startswith("CSM_QA")
    ].copy()

    # --- Cleaning pipeline ---
    df = original_df.copy()
    df = df[df["observability"] != "perceptif"]
    df = df[df["raw_variable_type"] != "textual"]
    df = df[df["id"] != -1]
    df = df.drop_duplicates(subset="raw_variable_name", keep="first")
    df = df.drop_duplicates(subset="id", keep="first")

    columns_to_keep = [
        "id", "raw_variable_name", "raw_variable_type",
        "Questions", "Choix de réponse "
    ]
    df = df[columns_to_keep]

    # Save cleaned CSV
    df.to_csv("codebook_study1.csv", index=False)
    print("✅ CSV cleaned and saved → codebook_study1.csv")

    # Markdown
    md_lines = []

    # --- Top explanatory block (NEW) ---
    md_lines.append("# Questionnaire – Study 1\n")
    md_lines.append(
        "> **Source information**\n"
        "> The “Source” indicates the reference of the scale or instrument that informed each item, "
        "whether the item was inspired by that measure, adapted from it, or uses the same wording. "
        "Sources are provided only for items originating from validated instruments.\n"
    )
    md_lines.append(
        "> **Note:** Questions marked with a star (*) have been selected during the feature selection "
        "phase and are used in the prediction model for Study 2.\n"
    )
    md_lines.append("")

    # ---------- NORMAL QUESTIONS ----------
    for i, row in enumerate(df.itertuples(index=False), start=1):
        qid = row.raw_variable_name

        STAR = " (*)" if qid in STARRED_IDS else ""

        md_lines.append(f"## Question {i}{STAR}")
        md_lines.append(f"**Question id :** `{qid}`\n")
        md_lines.append(f"**Type of variable :** {row.raw_variable_type}\n")
        md_lines.append(f"**Question content :** {row.Questions}\n")

        # --- Add source / URL ---
        source_val = sources_map.get(qid, "")
        if isinstance(source_val, str) and source_val.strip():
            url = extract_url(source_val)
            text_part = source_val.replace(url, "") if url else source_val
            if text_part.strip():
                md_lines.append(f"**Source :** {text_part.strip()}\n")
            if url:
                md_lines.append(f"**Url link :** [Open link]({url})\n")

        # Possible answers
        answers = row._4
        if pd.notna(answers) and str(answers).strip():
            answers = str(answers).strip()
            if ";" in answers:
                md_lines.append("**Possible answers :**")
                for a in [x.strip() for x in answers.split(";") if x.strip()]:
                    md_lines.append(f"- {a}")
                md_lines.append("")
            else:
                md_lines.append(f"**Possible answers :** {answers}\n")

        md_lines.append("---\n")

    # ---------- CSM_QA QUESTIONS ----------
    if not csm_df.empty:
        md_lines.append("# 14-item MHC-SF questions\n")

        for _, row in csm_df.iterrows():
            qid = row["raw_variable_name"]

            md_lines.append(f"## Question `{qid}`\n")
            md_lines.append(f"**Type of variable :** {row['raw_variable_type']}\n")
            md_lines.append(f"**Question content :** {row['Questions']}\n")

            source_val = sources_map.get(qid, "")
            if isinstance(source_val, str) and source_val.strip():
                url = extract_url(source_val)
                text_part = source_val.replace(url, "") if url else source_val
                if text_part.strip():
                    md_lines.append(f"**Source :** {text_part.strip()}\n")
                if url:
                    md_lines.append(f"**Url link :** [Open link]({url})\n")

            answers = row.get("Choix de réponse ", None)
            if pd.notna(answers) and str(answers).strip():
                answers = str(answers).strip()
                if ";" in answers:
                    md_lines.append("**Possible answers :**")
                    for a in [x.strip() for x in answers.split(";") if x.strip()]:
                        md_lines.append(f"- {a}")
                    md_lines.append("")
                else:
                    md_lines.append(f"**Possible answers :** {answers}\n")

            md_lines.append("---\n")

    # Write Markdown
    md_content = "\n".join(md_lines)
    Path("codebook_study1.md").write_text(md_content, encoding="utf-8")
    print("📄 Markdown created → codebook_study1.md")

    try:
        pypandoc.convert_text(
            md_content, to="pdf", format="md",
            outputfile="codebook_study1.pdf", extra_args=["--standalone"]
        )
        print("📘 PDF created → codebook_study1.pdf")
    except Exception as e:
        print("⚠️ PDF generation failed:", e)



# ============================================================
#                STUDY 2 — CLEANING FUNCTION
# ============================================================

def clean_study2_codebook():
    # Load CSVs
    questions = pd.read_csv("codebook_questions.csv")
    answers = pd.read_csv("codebook_answers.csv")
    groups = pd.read_csv("questions_matching_study2.csv", delimiter=';')

    # Load source mapping
    sources_df = pd.read_csv("codebook_study2_sources.csv")
    sources_map = dict(zip(sources_df["question_id"], sources_df["source"]))

    # Keep only groups found in matching file
    valid_groups = set(groups["group_id"].unique())
    questions = questions[questions["group_id"].isin(valid_groups)]

    merged = questions.merge(
        answers, on="question_id", how="left", validate="one_to_many"
    )

    merged = merged.sort_values(["group_id", "question_id"])
    groups = groups.sort_values("order")

    md_lines = []

    # --- Top explanatory block (NEW) ---
    md_lines.append("# Questionnaire – Study 2\n")
    md_lines.append(
        "> **Source information**\n"
        "> The “Source” indicates the reference of the scale or instrument that informed each item, "
        "whether the item was inspired by that measure, adapted from it, or uses the same wording. "
        "Sources are provided only for items originating from validated instruments.\n"
    )
    md_lines.append("")

    explanation_inserted = False

    # ---------- SECTIONS ----------
    for _, group in groups.iterrows():
        gid = group["group_id"]
        label = group["group_label"]

        md_lines.append(f"## {label}\n")

        group_q = merged[merged["group_id"] == gid]

        for qid, qdf in group_q.groupby("question_id"):
            question_content = qdf["question_content"].iloc[0]
            question_info = qdf["question_info"].iloc[0] if "question_info" in qdf.columns else ""

            # If question_info exists, prepend it
            if isinstance(question_info, str) and question_info.strip():
                question_content = f"{question_info.strip()} {question_content}"

            # Prefix for essaim
            if str(qid).startswith("essaim_"):
                question_content = (
                    "In the past month, how often have you felt… "
                    + question_content
                )

            form_id = qdf["form_id"].iloc[0]
            pilote_id = qdf["pilote_id"].iloc[0] if "pilote_id" in qdf.columns else None

            # HEADER
            md_lines.append(f"### Question id : `{qid}`\n")
            md_lines.append(f"**Form:** `{form_id}`\n")
            if pd.notna(pilote_id):
                md_lines.append(f"**Pilote ID:** `{pilote_id}`")

            md_lines.append(f"\n**Question content :** {question_content}\n")

            # --- Add source / URL ---
            source_val = sources_map.get(qid, "")
            if isinstance(source_val, str) and source_val.strip():
                url = extract_url(source_val)
                text_part = source_val.replace(url, "") if url else source_val
                if text_part.strip():
                    md_lines.append(f"**Source :** {text_part.strip()}\n")
                if url:
                    md_lines.append(f"**Url link :** [Open link]({url})\n")

            # Answers
            answers_list = (
                qdf["answer_content"].dropna().unique().tolist()
            )
            if answers_list:
                md_lines.append("**Possible answers :**")
                for a in answers_list:
                    md_lines.append(f"- {a}")
                md_lines.append("")

            md_lines.append("---\n")

        # Explanation stories insertion
        if not explanation_inserted and label.strip().lower() == "20 predictor questions".lower():
            md_lines.append("## Explanation stories\n")
            md_lines.append(
                "Depending on the experiment condition, the participant is redirected "
                "towards one of several explanation stories.\n"
            )
            md_lines.append("---\n")
            explanation_inserted = True

    # Write Markdown
    md_content = "\n".join(md_lines)
    Path("codebook_study2.md").write_text(md_content, encoding="utf-8")

    print("📄 Markdown created → codebook_study2.md")

    try:
        pypandoc.convert_text(
            md_content, to="pdf", format="md",
            outputfile="codebook_study2.pdf", extra_args=["--standalone"]
        )
        print("📘 PDF created → codebook_study2.pdf")
    except Exception as e:
        print("⚠️ PDF generation failed:", e)


def clean_merge_features():
    # Input
    FEATURE_SELECTION_PATH = (
        C.ML_PATH / "real" / C.FEATURE_SELECTION_FOLDER_NAME / "feature_library_v10"
    )
    FEATURE_LIBARY_PATH = (
        C.ML_PATH / "real" / C.FEATURE_LIBRARIES_FOLDER_NAME / "feature_library_v10"
    )
    feature_selection_filename = C.FEATURE_SELECTION_FILENAME.format("xgboost_k_20")

    lookup_df = pd.read_csv(FEATURE_LIBARY_PATH / C.FEATURE_LOOKUP_FILENAME)
    selection_df = pd.read_csv(FEATURE_SELECTION_PATH / feature_selection_filename)

    # Merge on 'feature_names'
    merged_df = pd.merge(
        lookup_df,
        selection_df,
        on="feature_names",
        how="inner",  # only keep features present in both files
    )

    # Output
    data_shared_path = Path(os.getenv("DATA_SHARED_PATH"))
    study1_path = data_shared_path / "Study 1"
    merged_df.to_csv(study1_path / "features.csv", index=False)

    print("✅ merged_feature_data.csv created successfully.")
    print("Shape:", merged_df.shape)
