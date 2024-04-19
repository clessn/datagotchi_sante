# Packages ---------------------------------------------------------------------
library(dplyr)

# Data -------------------------------------------------------------------------

## load raw data here

data_raw <- haven::read_sav("_SharedFolder_datagotchi-santé/data/raw/Datagotchi-Santé_Pilote_April 3, 2024_09.12.sav")

# Clean variables ---------------------------------------------------------

data_clean <- data.frame(id = 1:nrow(data_raw))

# Save it --------------------------------------------------------------------
saveRDS(data_clean, "_Shared_DatagotchiUS/data/cleaning_2024/data_clean.rds")