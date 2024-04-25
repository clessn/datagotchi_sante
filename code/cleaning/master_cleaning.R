# Packages ---------------------------------------------------------------------
library(dplyr)

# Data -------------------------------------------------------------------------

## load raw data here

data_raw <- haven::read_sav("_SharedFolder_datagotchi-santé/data/raw/Datagotchi-Santé_Pilote_April 25, 2024_15.59.sav")

# Clean variables ---------------------------------------------------------

data_clean <- data.frame(id = 1:nrow(data_raw))

# ATTENTION CHECK: Please select \"often\" for this answer to confirm that you are paying attention."
table(data_raw$autogestion_7)
attributes(data_raw$autogestion_7)
data_clean$attention_check_ok <- ifelse(data_raw$autogestion_7 == 3, 1, 0)
table(data_clean$attention_check_ok)

## ses -------------------------------------------------------------------------

source("code/cleaning/ses.R")


## lifestyle -------------------------------------------------------------------

source("code/cleaning/lifestyle.R")


## Bien-être -------------------------------------------------------------------

source("code/cleaning/bien_etre.R")


## Comp santé --------------------------------------------------------------

source("code/cleaning/comp_sante.R")

## Discrimination -----------------------------------------------------------

source("code/cleaning/discrimination.R")

# Save it --------------------------------------------------------------------

saveRDS(data_clean, "_SharedFolder_datagotchi-santé/data/clean/datagotchi-sante_clean.rds")

