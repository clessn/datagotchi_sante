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

attributes(data_raw$age)
table(data_raw$age)

data_clean$ses_age <- NA
data_clean$ses_age <- data_raw$age
table(data_clean$ses_age)

## Age group

data_clean$ses_age_group <- NA
data_clean$ses_age_group[data_raw$age < 18] <- "under_18"
data_clean$ses_age_group[data_raw$age >= 18 & data_raw$age <= 19] <- "18_19"
data_clean$ses_age_group[data_raw$age >= 20 & data_raw$age <= 24] <- "20_24"
data_clean$ses_age_group[data_raw$age >= 25 & data_raw$age <= 29] <- "25_29"
data_clean$ses_age_group[data_raw$age >= 30 & data_raw$age <= 34] <- "30_34"
data_clean$ses_age_group[data_raw$age >= 35 & data_raw$age <= 39] <- "35_39"
data_clean$ses_age_group[data_raw$age >= 40 & data_raw$age <= 44] <- "40_44"
data_clean$ses_age_group[data_raw$age >= 45 & data_raw$age <= 49] <- "45_49"
data_clean$ses_age_group[data_raw$age >= 50 & data_raw$age <= 54] <- "50_54"
data_clean$ses_age_group[data_raw$age >= 55 & data_raw$age <= 59] <- "55_59"
data_clean$ses_age_group[data_raw$age >= 60 & data_raw$age <= 64] <- "60_64"
data_clean$ses_age_group[data_raw$age >= 65 & data_raw$age <= 69] <- "65_69"
data_clean$ses_age_group[data_raw$age >= 70 & data_raw$age <= 74] <- "70_74"
data_clean$ses_age_group[data_raw$age >= 75 & data_raw$age <= 79] <- "75_79"
data_clean$ses_age_group[data_raw$age >= 80 & data_raw$age <= 84] <- "80_84"
data_clean$ses_age_group[data_raw$age > 84] <- "over_85"
data_clean$ses_age_group <- factor(data_clean$ses_age_group, levels = c("under_18",
                                                                        "18_19",
                                                                        "20_24",
                                                                        "25_29",
                                                                        "30_34",
                                                                        "35_39",
                                                                        "40_44",
                                                                        "45_49",
                                                                        "50_54",
                                                                        "55_59",
                                                                        "60_64",
                                                                        "65_69",
                                                                        "70_74",
                                                                        "75_79",
                                                                        "80_84",
                                                                        "over_85"))

table(data_clean$ses_age_group)

## Langue maternelle -----------------------------------------------------------

attributes(data_raw$langue_maternelle)
table(data_raw$langue_maternelle)
data_clean$ses_langue_maternelle <- NA
data_clean$ses_langue_maternelle[data_raw$langue_maternelle == 1] <- "francais"
data_clean$ses_langue_maternelle[data_raw$langue_maternelle == 2] <- "anglais"
data_clean$ses_langue_maternelle[data_raw$langue_maternelle == 3] <- "autre"
table(data_clean$ses_langue_maternelle)
data_clean$ses_langue_maternelle <- factor(data_clean$ses_langue_maternelle, levels = c("francais",
                                                                      "anglais",
                                                                      "autre"
                                                                            ))
table(data_clean$ses_langue_maternelle)

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


