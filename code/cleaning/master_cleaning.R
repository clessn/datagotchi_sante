# Packages ---------------------------------------------------------------------
library(dplyr)

# Data -------------------------------------------------------------------------

## load raw data here

data_raw <- haven::read_sav("_SharedFolder_datagotchi-santé/data/raw/Datagotchi-Santé_Pilote_April 3, 2024_09.12.sav")

# Clean variables ---------------------------------------------------------

data_clean <- data.frame(id = 1:nrow(data_raw))


## ses -------------------------------------------------------------------------

source("code/cleaning/ses.R")


## lifestyle -------------------------------------------------------------------

source("code/cleaning/lifestyle.R")


## Bien-être -------------------------------------------------------------------

source("code/cleaning/bien_etre.R")


# Save it --------------------------------------------------------------------

saveRDS(data_clean, "_SharedFolder_datagotchi-santé/data/clean/datagotchi-sante_clean.rds")

