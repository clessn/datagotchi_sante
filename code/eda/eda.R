# Experimental data analysis

# Load data
data_clean <- readRDS("_SharedFolder_datagotchi-santé/data/clean/datagotchi-sante_clean.rds")

# Check missing values
missing_values <- colSums(is.na(data_clean))
missing_values[missing_values > 0]

# Remove observations without score (because of NA in the questionnaire)
data <- data_clean %>%
  filter(!is.na(data_clean$score_norm))

# Check missing values
missing_values <- colSums(is.na(data))
missing_values[missing_values > 0]

# Aperçu des valeurs pour chaque variable
summary(data)
