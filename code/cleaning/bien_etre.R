# Bloc bien-Être

## CSM_Comparison --------------------------------------------------------------
attributes(data_raw$CSM_Comparison)
table(data_raw$CSM_Comparison)

data_clean$bien_etre_general_health <- (data_raw$CSM_Comparison - 1) / 4
table(data_clean$bien_etre_general_health)

## CSM_QA1 ---------------------------------------------------------------------
### CSM_QA1_1 ------------------------------------------------------------------
attributes(data_raw$CSM_QA1_1)
table(data_raw$CSM_QA1_1)

data_clean$bien_etre_felt_happy <- (data_raw$CSM_QA1_1 - 1) / 5
table(data_clean$bien_etre_felt_happy)

### CSM_QA1_2 ------------------------------------------------------------------
attributes(data_raw$CSM_QA1_2)
table(data_raw$CSM_QA1_2)

data_clean$bien_etre_interested_in_life <- (data_raw$CSM_QA1_2 - 1) / 5
table(data_clean$bien_etre_interested_in_life)

### CSM_QA1_3 ------------------------------------------------------------------
attributes(data_raw$CSM_QA1_3)
table(data_raw$CSM_QA1_3)

data_clean$bien_etre_satisfied_with_life <- (data_raw$CSM_QA1_3 - 1) / 5
table(data_clean$bien_etre_satisfied_with_life)

## CSM_QA2 -------------------------------------------------------------------
### CSM_QA2_1 ----------------------------------------------------------------
attributes(data_raw$CSM_QA2_1)
table(data_raw$CSM_QA2_1)

data_clean$bien_etre_important_contribution_society <- (data_raw$CSM_QA2_1 - 1) / 5
table(data_clean$bien_etre_important_contribution_society)

### CSM_QA2_2 ----------------------------------------------------------------
attributes(data_raw$CSM_QA2_2)
table(data_raw$CSM_QA2_2)

data_clean$bien_etre_sense_belonging_community <- (data_raw$CSM_QA2_2 - 1) / 5
table(data_clean$bien_etre_sense_belonging_community)

### CSM_QA2_3 ----------------------------------------------------------------
attributes(data_raw$CSM_QA2_3)
table(data_raw$CSM_QA2_3)

data_clean$bien_etre_society_becomes_better_place <- (data_raw$CSM_QA2_3 - 1) / 5
table(data_clean$bien_etre_society_becomes_better_place)

### CSM_QA2_4 ----------------------------------------------------------------
attributes(data_raw$CSM_QA2_4)
table(data_raw$CSM_QA2_4)

data_clean$bien_etre_people_fundamentally_good <- (data_raw$CSM_QA2_4 - 1) / 5
table(data_clean$bien_etre_people_fundamentally_good)

### CSM_QA2_5 ----------------------------------------------------------------
attributes(data_raw$CSM_QA2_5)
table(data_raw$CSM_QA2_5)

data_clean$bien_etre_society_makes_sense <- (data_raw$CSM_QA2_5 - 1) / 5
table(data_clean$bien_etre_society_makes_sense)

### CSM_QA2_6 ----------------------------------------------------------------
attributes(data_raw$CSM_QA2_6)
table(data_raw$CSM_QA2_6)

data_clean$bien_etre_like_personality <- (data_raw$CSM_QA2_6 - 1) / 5
table(data_clean$bien_etre_like_personality)

### CSM_QA2_7 ----------------------------------------------------------------
attributes(data_raw$CSM_QA2_7)
table(data_raw$CSM_QA2_7)

data_clean$bien_etre_handling_responsibilities <- (data_raw$CSM_QA2_7 - 1) / 5
table(data_clean$bien_etre_handling_responsibilities)

### CSM_QA2_8 ----------------------------------------------------------------
attributes(data_raw$CSM_QA2_8)
table(data_raw$CSM_QA2_8)

data_clean$bien_etre_warm_relationships_with_people <- (data_raw$CSM_QA2_8 - 1) / 5
table(data_clean$bien_etre_warm_relationships_with_people)

### CSM_QA2_9 ----------------------------------------------------------------
attributes(data_raw$CSM_QA2_9)
table(data_raw$CSM_QA2_9)

data_clean$bien_etre_better_person <- (data_raw$CSM_QA2_9 - 1) / 5
table(data_clean$bien_etre_better_person)

### CSM_QA2_10 ---------------------------------------------------------------
attributes(data_raw$CSM_QA2_10)
table(data_raw$CSM_QA2_10)



## PHQ4_1 ----------------------------------------------------------------------

attributes(data_raw$PHQ4_1)
table(data_raw$PHQ4_1)
data_clean$bien_etre_pleasure_doing_things <- NA
data_clean$bien_etre_pleasure_doing_things <- (data_raw$PHQ4_1 - 1) / 3
table(data_clean$bien_etre_pleasure_doing_things)


## PHQ4_2 ------------------------------------------------------------------

attributes(data_raw$PHQ4_2)
table(data_raw$PHQ4_2)
data_clean$bien_etre_sad <- NA
data_clean$bien_etre_sad <- (data_raw$PHQ4_2 - 1) / 3
table(data_clean$bien_etre_sad)


## PHQ4_3 ------------------------------------------------------------------

attributes(data_raw$PHQ4_3)
table(data_raw$PHQ4_3)
data_clean$bien_etre_nervous <- NA
data_clean$bien_etre_nervous <- (data_raw$PHQ4_3 - 1) / 3
table(data_clean$bien_etre_nervous)


## PHQ4_4 ------------------------------------------------------------------

attributes(data_raw$PHQ4_4)
table(data_raw$PHQ4_4)
data_clean$bien_etre_worries <- NA
data_clean$bien_etre_worries <- (data_raw$PHQ4_4 - 1) / 3
table(data_clean$bien_etre_worries)


## hsa_stress__vie -------------------------------------------------------------

attributes(data_raw$hsa_stress__vie)
table(data_raw$hsa_stress__vie)
data_clean$bien_etre_stress_vie <- NA
data_clean$bien_etre_stress_vie <- (data_raw$hsa_stress__vie - 1) / 4
table(data_clean$bien_etre_stress_vie)


## Maladies -------------------------------------------------------------------- 

attributes(data_raw$maladies_1)


