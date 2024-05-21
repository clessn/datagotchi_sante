library(dplyr)

# Read the SPSS data file and filter for respondents with Finished variable set to TRUE
data <- haven::read_sav("_SharedFolder_datagotchi-santé/data/raw/Datagotchi-Santé_Pilote_May 21, 2024_11.55.sav") %>%
  filter(Finished == 1)

data_missing_values <- sondr::qualtrics_na_counter(data)

ggplot2::ggsave("_SharedFolder_datagotchi-santé/data/graphs/na_check.png")
