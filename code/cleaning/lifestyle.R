# Bloc lifestyle ---------------------------------------------------------------

## Pets ------------------------------------------------------------------------



## Activité physique -----------------------------------------------------------



## Freq_physique ---------------------------------------------------------------



## Transport -------------------------------------------------------------------



## Car model -------------------------------------------------------------------



## Consumption -----------------------------------------------------------------




## Coffee ----------------------------------------------------------------------




## Meat ------------------------------------------------------------------------

attributes(data_raw$meat)
table(data_raw$meat)
data_clean$lifestyle_meat <- NA
data_clean$lifestyle_meat <- (data_raw$meat - 1) / 6
table(data_clean$lifestyle_meat)

## Alcool pref -----------------------------------------------------------------




## Smoking ---------------------------------------------------------------------





## Cannabis --------------------------------------------------------------------



## Hunting ---------------------------------------------------------------------



## Fishing ---------------------------------------------------------------------



## Act_motorized ---------------------------------------------------------------



## Friends ---------------------------------------------------------------------




## Volunteer -------------------------------------------------------------------




## Museum ----------------------------------------------------------------------




## Nature ----------------------------------------------------------------------



## Movie pref ------------------------------------------------------------------





## Style -----------------------------------------------------------------------

attributes(data_raw$style)
table(data_raw$style)
data_clean$lifestyle_style <- NA
data_clean$lifestyle_style[data_raw$style == 1] <- "Hippie"
data_clean$lifestyle_style[data_raw$style == 2] <- "Elegant"
data_clean$lifestyle_style[data_raw$style == 3] <- "Classical"
data_clean$lifestyle_style[data_raw$style == 4] <- "Casual"
data_clean$lifestyle_style[data_raw$style == 5] <- "Formal"
data_clean$lifestyle_style[data_raw$style == 6] <- "Punk"
data_clean$lifestyle_style[data_raw$style == 7] <- "Rock"
data_clean$lifestyle_style[data_raw$style == 8] <- "Sporty"
data_clean$lifestyle_style[data_raw$style == 9] <- "Other"
data_clean$lifestyle_style <- factor(data_clean$lifestyle_style)
table(data_clean$lifestyle_style)

## Style altermatif


## Music pref ------------------------------------------------------------------


## Temps écran -----------------------------------------------------------------



