import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from app.ml.constants import Constants as C

# Load the .env file
load_dotenv()


import pandas as pd
from pathlib import Path

import pandas as pd
from pathlib import Path
import pypandoc

def clean_study1_codebook():
    # --- Load ---
    original_df = pd.read_csv(C.CODEBOOK_PATH / "frozen_codebook_october_15.csv")

    # Extract all CSM_QA* rows BEFORE filtering
    csm_df = original_df[
        original_df["raw_variable_name"].astype(str).str.startswith("CSM_QA")
    ].copy()

    # --- Begin normal cleaning pipeline ---
    df = original_df.copy()

    # Keep only observable variables
    df = df[df["observability"] != "perceptif"]
    df = df[df["raw_variable_type"] != "textual"]

    # Remove duplicated ids
    df = df[df["id"] != -1]
    df = df.drop_duplicates(subset="raw_variable_name", keep="first")
    df = df.drop_duplicates(subset="id", keep="first")

    # Keep only needed columns
    columns_to_keep = [
        "id",
        "raw_variable_name",
        "raw_variable_type",
        "Questions",
        "Choix de réponse ",
    ]
    df = df[columns_to_keep]

    # --- Save cleaned CSV ---
    df.to_csv("codebook_study1.csv", index=False)
    print("✅ CSV cleaned and saved → codebook_study1.csv")

    # --- Create source CSV ---
    sources_df = pd.DataFrame({
        "question_id": df["raw_variable_name"],
        "question_content": df["Questions"],
        "source": ""
    })

    # Add CSM_QA questions at the end
    if not csm_df.empty:
        csm_sources = pd.DataFrame({
            "question_id": csm_df["raw_variable_name"],
            "question_content": csm_df["Questions"],
            "source": ""
        })
        sources_df = pd.concat([sources_df, csm_sources], ignore_index=True)

    sources_df.to_csv("codebook_study1_sources.csv", index=False)
    print("🗂️ Sources CSV created → codebook_study1_sources.csv")

    # --- Generate Markdown ---
    md_lines = []
    md_lines.append("# Questionnaire – Study 1\n")

    # Normal questions
    for i, row in enumerate(df.itertuples(index=False), start=1):
        md_lines.append(f"## Question {i}")
        md_lines.append(f"**Question id :** `{row.raw_variable_name}`\n")
        md_lines.append(f"**Type of variable :** {row.raw_variable_type}\n")

        # UPDATED HERE
        md_lines.append(f"**Question content :** {row.Questions}\n")

        answers = row._4  # Choix de réponse
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

    # Append CSM_QA questions
    if not csm_df.empty:
        md_lines.append("# Additional CSM Questions\n")

        for _, row in csm_df.iterrows():
            md_lines.append(f"## Question `{row['raw_variable_name']}`\n")
            md_lines.append(f"**Type of variable :** {row['raw_variable_type']}\n")

            # UPDATED HERE
            md_lines.append(f"**Question content :** {row['Questions']}\n")

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

    md_content = "\n".join(md_lines)
    Path("codebook_study1.md").write_text(md_content, encoding="utf-8")
    print("📄 Markdown created → codebook_study1.md")

    # --- Convert to PDF ---
    try:
        pypandoc.convert_text(
            md_content,
            to="pdf",
            format="md",
            outputfile="codebook_study1.pdf",
            extra_args=["--standalone"],
        )
        print("📘 PDF created → codebook_study1.pdf")
    except Exception as e:
        print("⚠️ PDF generation failed. Check if pandoc + pdflatex are installed.")
        print("Error:", e)



# ============================================================
#                STUDY 2 — CLEANING FUNCTION
# ============================================================

def clean_study2_codebook():
    # --- Load CSVs ---
    questions = pd.read_csv("codebook_questions.csv")
    answers = pd.read_csv("codebook_answers.csv")
    groups = pd.read_csv("questions_matching_study2.csv", delimiter=';')

    # Keep only valid groups
    valid_groups = set(groups["group_id"].unique())
    questions = questions[questions["group_id"].isin(valid_groups)]

    # Merge questions with answers
    merged = questions.merge(
        answers,
        on="question_id",
        how="left",
        validate="one_to_many"
    )

    merged = merged.sort_values(["group_id", "question_id"])
    groups = groups.sort_values("order")

    source_rows = []
    explanation_inserted = False

    md_lines = []
    md_lines.append("# Questionnaire – Study 2\n")

    for _, group in groups.iterrows():
        gid = group["group_id"]
        label = group["group_label"]

        md_lines.append(f"## {label}\n")
        group_q = merged[merged["group_id"] == gid]

        for qid, qdf in group_q.groupby("question_id"):
            question_text = qdf["question_content"].iloc[0]

            # Prefix for essaim questions
            if str(qid).startswith("essaim_"):
                question_text = (
                    "In the past month, how often have you felt… "
                    + str(question_text)
                )

            source_rows.append({
                "question_id": qid,
                "question_content": question_text,
                "source": ""
            })

            form_id = qdf["form_id"].iloc[0]
            pilote_id = qdf["pilote_id"].iloc[0] if "pilote_id" in qdf.columns else None

            md_lines.append(f"### Question `{qid}`\n")
            md_lines.append(f"**Form ID:** `{form_id}`\n")
            if pd.notna(pilote_id):
                md_lines.append(f"**Pilote ID:** `{pilote_id}`")

            # UPDATED HERE
            md_lines.append(f"\n**Question content :** {question_text}\n")

            answers_list = (
                qdf["answer_content"]
                .dropna()
                .unique()
                .tolist()
            )
            if answers_list:
                md_lines.append("**Possible answers :**")
                for a in answers_list:
                    md_lines.append(f"- {a}")
                md_lines.append("")

            md_lines.append("---\n")

        # Insert Explanation stories after correct section
        if not explanation_inserted and label.strip().lower() == "20 predictor questions".lower():
            md_lines.append("## Explanation stories\n")
            md_lines.append(
                "Depending on the experiment condition, the participant is redirected "
                "towards one of several explanation stories.\n"
            )
            md_lines.append("---\n")
            explanation_inserted = True

    md_content = "\n".join(md_lines)
    Path("codebook_study2.md").write_text(md_content, encoding="utf-8")
    print("📄 Markdown created → codebook_study2.md")

    # Save source CSV
    sources_df = pd.DataFrame(source_rows)
    sources_df.to_csv("codebook_study2_sources.csv", index=False)
    print("🗂️ Sources CSV created → codebook_study2_sources.csv")

    # PDF
    try:
        pypandoc.convert_text(
            md_content,
            to="pdf",
            format="md",
            outputfile="codebook_study2.pdf",
            extra_args=["--standalone"],
        )
        print("📘 PDF created → codebook_study2.pdf")
    except Exception as e:
        print("⚠️ PDF generation failed. Check if pandoc + pdflatex are installed.")
        print("Error:", e)


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
