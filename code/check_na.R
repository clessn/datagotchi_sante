library(ggplot2)
library(haven)
library(dplyr)
library(stringr)

# Read the SPSS data file and filter for respondents with Finished variable set to TRUE
data <- haven::read_sav("_SharedFolder_datagotchi-santé/data/raw/Datagotchi-Santé_Pilote_April 25, 2024_15.59.sav") %>%
  filter(Finished == 1)

data_text_columns <- data %>%
  select(ends_with("_TEXT")) %>% 
  mutate(across(everything(), ~na_if(., "")))

data <- data %>%
  select(-ends_with("_TEXT"))

data <- cbind(data, data_text_columns)

# Detect and group variable names by removing numeric and text suffixes
variable_groups <- names(data) %>%
  str_replace("_\\d+(_TEXT)?$", "") %>%
  unique()

# Create a datagrame to store the results
data_na_results <- data.frame(variable = variable_groups)

data_na_results$na_count <- NA
data_na_results$na_percentage <- NA

for (i in 1:nrow(data_na_results)) {
 
  prefix <- data_na_results$variable[i]
  
  # Select columns that start with the prefix and end with either a number or "_TEXT"
  data_loop <- data  %>%  
    select(starts_with(prefix))

    
  
  data_loop$na <- NA
  # Create a new column 'na', checking if all selected fields in a row are NA

  for (j in 1:nrow(data_loop)) {
    # Initialize a counter for NA values in the first row
    na_count <- 0

    # Loop through each column of the first row
    for (k in 1:ncol(data_loop)) {
      if (is.na(data_loop[j, k])) {
        na_count <- na_count + 1
      }
    }

    if (na_count == ncol(data_loop)) {
      data_loop$na[j] <- 0
    } else {
      data_loop$na[j] <- 1
    }
  }
  
  # Calculate the sum of 'na' column
  na_sum <- sum(data_loop$na)
  
  # Assign the sum to the corresponding entry in data_na_results
  data_na_results$na_count[i] <- as.numeric(na_sum)
  data_na_results$na_percentage[i] <- 100 - (na_sum / nrow(data_loop) * 100)

}

# Plot each variable in descending order with x = variable and y = na_percent. Make it coord_flip()

ggplot(data = subset(data_na_results, na_percentage > 0), aes(x = reorder(variable, na_percentage), y = na_percentage)) +
  geom_bar(stat = "identity", fill = "#e923c8") +
  coord_flip() +
  clessnize::theme_clean_dark() +
  labs(x = "Groupe de variable", y = "Pourcentage de données manquantes", title = "Pourcentage de données manquantes \npar groupe de variable")




ggsave("_SharedFolder_datagotchi-santé/data/graphs/na_check.png")