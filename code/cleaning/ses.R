# Bloc SES

## Genre -----------------------------------------------------------------------


## Orientation sexuelle --------------------------------------------------------


## Âge -------------------------------------------------------------------------



## Langue maternelle -----------------------------------------------------------



## Occupation ------------------------------------------------------------------




## Travail emploi --------------------------------------------------------------




## Travail domaine -------------------------------------------------------------





## Travail heure ---------------------------------------------------------------





## Télétravail heure -----------------------------------------------------------






## Revenu ----------------------------------------------------------------------






## Perception revenu -----------------------------------------------------------





## Éducation -------------------------------------------------------------------



## Pays origine ----------------------------------------------------------------




## Origines ethniques ----------------------------------------------------------

attributes(data_raw$origines_ethniques)
table(data_raw$origines_ethniques)
data_clean$ses_origines_ethniques <- NA
data_clean$ses_origines_ethniques[data_raw$origines_ethniques == 1] <- "white"
data_clean$ses_origines_ethniques[data_raw$origines_ethniques == 2] <- "black"
data_clean$ses_origines_ethniques[data_raw$origines_ethniques == 3] <- "indigenous"
data_clean$ses_origines_ethniques[data_raw$origines_ethniques == 4] <- "asian"
data_clean$ses_origines_ethniques[data_raw$origines_ethniques == 5] <- "hispanic"
data_clean$ses_origines_ethniques[data_raw$origines_ethniques == 6] <- "arab"
data_clean$ses_origines_ethniques[data_raw$origines_ethniques == 7] <- "other"
data_clean$ses_origines_ethniques <- factor(data_clean$ses_origines_ethniques, levels = c("white", "black", "indigenous", "asian", "hispanic", "arab", "other"))
table(data_clean$ses_origines_ethniques)

## visible minority

data_clean$ses_visible_minority <- NA
data_clean$ses_visible_minority[data_raw$origines_ethniques == 1] <- 0
data_clean$ses_visible_minority[data_raw$origines_ethniques != 1] <- 1
table(data_clean$ses_visible_minority)


## Religion --------------------------------------------------------------------

attributes(data_raw$religion)
table(data_raw$religion)
data_clean$ses_religion <- NA
data_clean$ses_religion[data_raw$religion == 1] <- "atheist"
data_clean$ses_religion[data_raw$religion == 2] <- "agnostic"
data_clean$ses_religion[data_raw$religion == 3] <- "buddhist"
data_clean$ses_religion[data_raw$religion == 4] <- "hindu"
data_clean$ses_religion[data_raw$religion == 5] <- "judaism"
data_clean$ses_religion[data_raw$religion == 6] <- "muslim"
data_clean$ses_religion[data_raw$religion == 7] <- "sikhism"
data_clean$ses_religion[data_raw$religion == 8] <- "catholic"
data_clean$ses_religion[data_raw$religion == 9] <- "protestant"
data_clean$ses_religion[data_raw$religion == 10] <- "orthodox"
data_clean$ses_religion[data_raw$religion == 11] <- "other"
data_clean$ses_religion <- factor(data_clean$ses_religion, levels = c("atheist", "agnostic", "buddhist", "hindu", "judaism", "muslim", "sikhism", "catholic", "protestant", "orthodox", "other"))
table(data_clean$ses_religion)

## Religiosité -----------------------------------------------------------------

attributes(data_raw$religiosite_1)
table(data_raw$religiosite_1)
data_clean$ses_religiosite <- NA
data_clean$ses_religiosite <- data_raw$religiosite_1 / 100
table(data_clean$ses_religiosite)

## Enfants ---------------------------------------------------------------------

attributes(data_raw$enfants)
table(data_raw$enfants)
data_clean$ses_enfants <- NA
data_clean$ses_enfants[data_raw$enfants == 1] <- "0"
data_clean$ses_enfants[data_raw$enfants == 2] <- "1"
data_clean$ses_enfants[data_raw$enfants == 3] <- "2"
data_clean$ses_enfants[data_raw$enfants == 4] <- "3"
data_clean$ses_enfants[data_raw$enfants == 5] <- "4"
data_clean$ses_enfants[data_raw$enfants == 6] <- "5 or more"
data_clean$ses_enfants <- factor(data_clean$ses_enfants, levels = c("0", "1", "2", "3", "4", "5 or more"))  
table(data_clean$ses_enfants)

## Enfants bin

data_clean$ses_enfants_bin <- NA
data_clean$ses_enfants_bin[data_raw$enfants == 0] <- 0
data_clean$ses_enfants_bin[data_raw$enfants != 0] <- 1
table(data_clean$ses_enfants_bin)

## Statut marital --------------------------------------------------------------

attributes(data_raw$married)
table(data_raw$married)
data_clean$ses_marrital_status <- NA
data_clean$ses_marrital_status[data_raw$married == 1] <- "single"
data_clean$ses_marrital_status[data_raw$married == 2] <- "married"
data_clean$ses_marrital_status[data_raw$married == 3] <- "common_law"
data_clean$ses_marrital_status[data_raw$married == 4] <- "widow"
data_clean$ses_marrital_status[data_raw$married == 5] <- "divorced"
data_clean$ses_marrital_status <- factor(data_clean$ses_marrital_status, levels = c("single", "married", "common_law", "widow", "divorced"))
table(data_clean$ses_marrital_status)

## Status marital married

data_clean$ses_married <- NA
data_clean$ses_married[data_raw$married == 2] <- 1
data_clean$ses_married[data_raw$married != 2] <- 0
table(data_clean$ses_married)

## status marital single

data_clean$ses_single <- NA
data_clean$ses_single[data_raw$married == 1] <- 1
data_clean$ses_single[data_raw$married != 1] <- 0
table(data_clean$ses_single)

## Poids -----------------------------------------------------------------------
## This takes the value from the data_raw$poids_1_TEXT variable and converts it to a numeric value then converts it to pounds (it's in kilo)
## then it takes the value from the data_raw$poids_2_TEXT variable and converts it to a numeric value.

attributes(data_raw$poids)
table(data_raw$poids, useNA = "ifany")
table(data_raw$poids_1_TEXT, useNA = "ifany")
table(data_raw$poids_2_TEXT, useNA = "ifany")
data_clean$ses_poids <- NA
data_clean$ses_poids <- ifelse(data_raw$poids == 1 & !is.na(data_raw$poids_1_TEXT), as.numeric(data_raw$poids_1_TEXT) * 2.20462, data_clean$ses_poids)
data_clean$ses_poids <- ifelse(data_raw$poids == 2 & !is.na(data_raw$poids_2_TEXT), as.numeric(data_raw$poids_2_TEXT), data_clean$ses_poids)
table(data_clean$ses_poids)

## Taille ----------------------------------------------------------------------


## Code postal -----------------------------------------------------------------

attributes(data_raw$code_postal)
table(data_raw$code_postal)
data_clean$ses_code_postal <- NA
data_clean$ses_code_postal <- data_raw$code_postal
table(data_clean$ses_code_postal)


## Travail deplacement ---------------------------------------------------------




## Milieu vie ------------------------------------------------------------------





## Habitation ------------------------------------------------------------------




## Province --------------------------------------------------------------------




## 


