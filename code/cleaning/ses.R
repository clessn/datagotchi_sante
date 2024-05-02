# Bloc SES

## Genre -----------------------------------------------------------------------

## Male

attributes(data_raw$genre)
table(data_raw$genre)
data_clean$ses_male <- NA
data_clean$ses_male[data_raw$genre == 1] <- 1
data_clean$ses_male[data_raw$genre != 1] <- 0
table(data_clean$ses_male)

## Female

data_clean$ses_female <- NA
data_clean$ses_female[data_raw$genre == 2] <- 1
data_clean$ses_female[data_raw$genre != 2] <- 0
table(data_clean$ses_female)

## Factor 

data_clean$ses_genre <- NA
data_clean$ses_genre[data_raw$genre == 1] <- "male"
data_clean$ses_genre[data_raw$genre == 2] <- "female"
data_clean$ses_genre[data_raw$genre == 3] <- "transgender_male"
data_clean$ses_genre[data_raw$genre == 4] <- "transgender_woman"
data_clean$ses_genre[data_raw$genre == 5] <- "non_binary"
data_clean$ses_genre[data_raw$genre == 6] <- "queer"
data_clean$ses_genre[data_raw$genre == 7] <- "agender"
data_clean$ses_genre[data_raw$genre == 8] <- "other"
table(data_clean$ses_genre)

## Orientation sexuelle --------------------------------------------------------

attributes(data_raw$orientation)
data_clean$ses_sexual_orientation <- NA
data_clean$ses_sexual_orientation[data_raw$orientation == 1] <- "heterosexual"
data_clean$ses_sexual_orientation[data_raw$orientation == 2] <- "bisexual"
data_clean$ses_sexual_orientation[data_raw$orientation == 3] <- "gay_lesbian"
data_clean$ses_sexual_orientation[data_raw$orientation == 4] <- "other"
data_clean$ses_sexual_orientation <- factor(data_clean$ses_sexual_orientation, levels = c("heterosexual",
                                                                                          "bisexual",
                                                                                          "gay_lesbian",
                                                                                          "other"))
table(data_clean$ses_sexual_orientation)

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






## Religion --------------------------------------------------------------------






## Religiosité -----------------------------------------------------------------





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





## Poids -----------------------------------------------------------------------





## Taille ----------------------------------------------------------------------





## Code postal -----------------------------------------------------------------





## Travail deplacement ---------------------------------------------------------






## Milieu vie ------------------------------------------------------------------





## Habitation ------------------------------------------------------------------




## Province --------------------------------------------------------------------




## 


