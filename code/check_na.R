library(ggplot2)
library(haven)

# Read the SPSS data file
data <- haven::read_sav("_SharedFolder_datagotchi-santé/data/raw/Datagotchi-Santé_Pilote_April 25, 2024_15.59.sav")

# Calculate missing values
missing_values <- colSums(is.na(data))

# Calculate percentage of missing values
percentage_missing <- missing_values / nrow(data) * 100

# Create a data frame with variable names and missing percentages
missing_data <- data.frame(
  variable = names(percentage_missing),
  missing_count = missing_values,
  percentage_missing = percentage_missing
)

# Sort the data frame by percentage of missing values
missing_data <- missing_data[order(missing_data$percentage_missing, decreasing = TRUE), ]

# Create ggplot
ggplot(missing_data, aes(x = reorder(variable, percentage_missing), y = percentage_missing)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  coord_flip() +
  labs(x = "Variable", y = "Percentage of Missing Values", title = "Percentage of Missing Values by Variable")

