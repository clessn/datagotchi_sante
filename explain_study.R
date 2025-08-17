###############
# Packages 
###############

# packages installation for the first time only
install.packages("readr")
install.packages("dotenv")
install.packages("lubridate")

# packages loading
library(readr) # reading csv files
library(dotenv) # loading environment variables from .env file
library(lubridate) # for date manipulation

###############
# Loading data 
###############

# read path from environment variable
data_result_path <- Sys.getenv("DATA_RESULT_PATH")

# build the path to the file with results
clean_results_file_path <- file.path(data_result_path, "clean", "clean_results.csv")

# read file
clean_results <- read_csv(clean_results_file_path)

# convert columns to appropriate types
# duration, remove date part and convert to duration
clean_results$study_duration <- hms(sub(".* ", "", clean_results$study_duration))
# factor
cols_to_factor <- c(
  "explain_type",
  "sociodemo_01",
  "sociodemo_02",
  "sociodemo_03",
  "sociodemo_05",
  "sociodemo_07",
  "sociodemo_08"
)
clean_results[cols_to_factor] <- lapply(clean_results[cols_to_factor], as.factor)

# show the head of the data
head(clean_results)
sapply(clean_results, class)

###############
# Manipulation checks
###############

# Manipulation model for visual
manip_model_visual <- lm(manipulation_visual ~ relevel(explain_type, ref = "explain_visual"), data = clean_results)
summary(manip_model_visual)

# Manipulation model for textual
manip_model_textual <- lm(manipulation_textual ~ relevel(explain_type, ref = "explain_textual"), data = clean_results)
summary(manip_model_textual)

# Manipulation model for quantitative
manip_model_quantitative <- lm(manipulation_quantitative ~ relevel(explain_type, ref = "explain_quantitative"), data = clean_results)
summary(manip_model_quantitative)

# Manipulation model for interactive
manip_model_interactive <- lm(manipulation_interactive ~ relevel(explain_type, ref = "explain_interactive"), data = clean_results)
summary(manip_model_interactive)

# Manipulation model for contextual
manip_model_contextual <- lm(manipulation_contextual ~ relevel(explain_type, ref = "explain_contextual"), data = clean_results)
summary(manip_model_contextual)

###############
# Main models
###############

# To complete