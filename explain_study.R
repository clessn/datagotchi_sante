library(readr)

# Reand path from environment variable
data_result_path <- Sys.getenv("DATA_RESULT_PATH")

# Build the path to the file with results
clean_results_file_path <- file.path(data_result_path, "clean", "clean_results.csv")

# Read file
clean_results <- read_csv(file_path)

# Show the head of the data
head(clean_results)