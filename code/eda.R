
data <- data_raw

# Ajouter la colonne de score
data$score_norm <- data_score$score_norm

# On ne prend que les répondants qui ont fini le questionnaire
data <- data %>%
  filter(Finished == 1)

# Vérifier les valeurs manquantes
missing_values <- colSums(is.na(data))
missing_values[missing_values > 0]

# Retirer les répondants qui n'ont pas de score (car NA dans le questionnaire)
data <- data %>%
  filter(!is.na(data$score_norm))

# Aperçu des valeurs pour chaque variable
summary(data)
