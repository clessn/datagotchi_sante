# On ne prend que les répondants qui ont fini le questionnaire
data <- data_raw %>%
  filter(Finished == 1)

# Aperçu des valeurs pour chaque variable
summary(data)

# Vérifier les valeurs manquantes
missing_values <- colSums(is.na(data))
missing_values[missing_values > 0]

