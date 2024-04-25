# Bloc bien-Être

## CSM_Comparison --------------------------------------------------------------



## CSM_QA1 ---------------------------------------------------------------------



## PHQ4_1 ----------------------------------------------------------------------

attributes(data_raw$PHQ4_1)
table(data_raw$PHQ4_1)
data_clean$bien_etre_pleasure_doing_things <- NA
data_clean$bien_etre_pleasure_doing_things <- (data_raw$PHQ4_1 - 1) / 3
table(data_clean$bien_etre_pleasure_doing_things)

## hsa_stress__vie -------------------------------------------------------------




## Maladies -------------------------------------------------------------------- 