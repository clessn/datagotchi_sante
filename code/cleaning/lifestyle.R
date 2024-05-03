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

attributes(data_raw$alcool_pref)
table(data_raw$alcool_pref)
data_clean$lifestyle_alcool_pref <- NA
data_clean$lifestyle_alcool_pref[data_raw$alcool_pref == 1] <- "Craft or microbrewery beer"
data_clean$lifestyle_alcool_pref[data_raw$alcool_pref == 2] <- "Regular beer"
data_clean$lifestyle_alcool_pref[data_raw$alcool_pref == 3] <- "Spirit drink"
data_clean$lifestyle_alcool_pref[data_raw$alcool_pref == 4] <- "Cocktail"
data_clean$lifestyle_alcool_pref[data_raw$alcool_pref == 5] <- "White wine"
data_clean$lifestyle_alcool_pref[data_raw$alcool_pref == 6] <- "Sparkling wine or champagne"
data_clean$lifestyle_alcool_pref[data_raw$alcool_pref == 7] <- "Rosé wine"
data_clean$lifestyle_alcool_pref[data_raw$alcool_pref == 8] <- "Red wine"
data_clean$lifestyle_alcool_pref[data_raw$alcool_pref == 9] <- "I do not drink alcohol"
data_clean$lifestyle_alcool_pref <- factor(data_clean$lifestyle_alcool_pref)
table(data_clean$lifestyle_alcool_pref)


## Smoking ---------------------------------------------------------------------

attributes(data_raw$smoking)
table(data_raw$smoking)
data_clean$lifestyle_smoking_freq <- NA
data_clean$lifestyle_smoking_freq <- (data_raw$smoking - 1) / 6
table(data_clean$lifestyle_smoking_freq)




## Cannabis --------------------------------------------------------------------

attributes(data_raw$cannabis)
table(data_raw$cannabis)
data_clean$lifestyle_cannabis <- NA
data_clean$lifestyle_cannabis <- (data_raw$cannabis - 1) / 6
table(data_clean$lifestyle_cannabis)


## Hunting ---------------------------------------------------------------------

attributes(data_raw$act_hunting)
table(data_raw$act_hunting)
data_clean$lifestyle_hunting <- NA
data_clean$lifestyle_hunting <- (data_raw$act_hunting - 1) / 4
table(data_clean$lifestyle_hunting)

## Fishing ---------------------------------------------------------------------

attributes(data_raw$act_fishing)
table(data_raw$act_fishing)
data_clean$lifestyle_fishing <- NA
data_clean$lifestyle_fishing <- (data_raw$act_fishing - 1) / 4
table(data_clean$lifestyle_fishing)


## Act_motorized ---------------------------------------------------------------

attributes(data_raw$act_motorized)
table(data_raw$act_motorized)
data_clean$lifestyle_motorized <- NA
data_clean$lifestyle_motorized <- (data_raw$act_motorized - 1) / 4
table(data_clean$lifestyle_motorized)

## Friends ---------------------------------------------------------------------

attributes(data_raw$act_friends)
table(data_raw$act_friends)
data_clean$lifestyle_friends_activity <- NA
data_clean$lifestyle_friends_activity <- (data_raw$act_friends - 1) / 4
table(data_clean$lifestyle_friends_activity)



## Volunteer -------------------------------------------------------------------

attributes(data_raw$act_volunteer)
table(data_raw$act_volunteer)
data_clean$lifestyle_volunteer <- NA
data_clean$lifestyle_volunteer <- (data_raw$act_volunteer - 1) / 4
table(data_clean$lifestyle_volunteer)



## Museum ----------------------------------------------------------------------

attributes(data_raw$act_museum)
table(data_raw$act_museum)
data_clean$lifestyle_museum <- NA
data_clean$lifestyle_museum <- (data_raw$act_museum - 1) / 4
table(data_clean$lifestyle_museum)


## Nature ----------------------------------------------------------------------

attributes(data_raw$act_nature_1)
table(data_raw$act_nature_1)
data_clean$lifestyle_nature_may_september <- NA
data_clean$lifestyle_nature_may_september <- (data_raw$act_nature_1 - 1) / 4
table(data_clean$lifestyle_nature_may_september)

attributes(data_raw$act_nature_2)
table(data_raw$act_nature_2)
data_clean$lifestyle_nature_october_april <- NA
data_clean$lifestyle_nature_october_april <- (data_raw$act_nature_2 - 1) / 4
table(data_clean$lifestyle_nature_october_april)


## Movie pref ------------------------------------------------------------------

table(data_raw$movie_pref)
data_clean$lifestyle_movie_pref <- (data_raw$movie_pref)
table(data_clean$lifestyle_movie_pref)


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

## Style autre-----------------------------------------------------------------------

attributes(data_raw$style_9_TEXT)
table(data_raw$style_9_TEXT)
data_clean$lifestyle_style_other <- NA
data_clean$lifestyle_style_other <- (data_raw$style_9_TEXT)
table(data_clean$lifestyle_style_other)

## Style altermatif



## Music pref ------------------------------------------------------------------

attributes(data_raw$music_pref)
table(data_raw$music_pref)
data_clean$lifestyle_music_pref <- NA
data_clean$lifestyle_music_pref <- (data_raw$music_pref)
table(data_clean$lifestyle_music_pref)

## Temps écran -----------------------------------------------------------------

# temps__cran__1 -----------------------------------------

attributes(data_raw$temps__cran__1)
table(data_raw$temps__cran__1)
data_clean$lifestyle_temps_ecran_semaine_travail <- NA


for (i in 1:nrow(data_raw)) {
  screen_time_str <- data_raw$temps__cran__1[i]  # Store the current value in a variable for easier handling
  
  # Clean up the string by removing all non-numeric and non-delimiter characters except delimiters
  clean_str <- gsub("[^0-9/_ -]", "", screen_time_str)
  
  if (grepl("[/_ -]", clean_str)) {
    # If there's any of the specified delimiters, split the string
    num_parts <- strsplit(clean_str, "[/_ -]")[[1]]
    num_values <- as.numeric(num_parts)  # Convert to numeric
    if (any(is.na(num_values))) {
      # Handle any NA values that may result from conversion (e.g., empty strings)
      num_values <- num_values[!is.na(num_values)]
    }
    if (length(num_values) > 0) {
      data_clean$lifestyle_temps_ecran_semaine_travail[i] <- max(num_values, na.rm = TRUE)  # Assign the maximum value if non-empty
    } else {
      # Assign a default value or handle empty num_values vector appropriately
      data_clean$lifestyle_temps_ecran_semaine_travail[i] <- NA  # Or some other default or error handling
    }
  } else if (grepl("min", screen_time_str)) {
    # If "min" is found, convert from minutes to hours
    data_clean$lifestyle_temps_ecran_semaine_travail[i] <- as.numeric(gsub("[^0-9]", "", screen_time_str)) / 60
  } else {
    # Assume the input is in hours and just remove non-numeric characters
    data_clean$lifestyle_temps_ecran_semaine_travail[i] <- as.numeric(gsub("[^0-9]", "", screen_time_str))
  }
}

table(data_clean$lifestyle_temps_ecran_semaine_travail) 


# temps__cran__2 ---------------------------------------

attributes(data_raw$temps__cran__2)
table(data_raw$temps__cran__2)
data_clean$lifestyle_temps_ecran_finsemaine_travail <- NA


for (i in 1:nrow(data_raw)) {
  screen_time_str <- data_raw$temps__cran__2[i]  # Store the current value in a variable for easier handling
  
  # Clean up the string by removing all non-numeric and non-delimiter characters except delimiters
  clean_str <- gsub("[^0-9/_ -]", "", screen_time_str)
  
  if (grepl("[/_ -]", clean_str)) {
    # If there's any of the specified delimiters, split the string
    num_parts <- strsplit(clean_str, "[/_ -]")[[1]]
    num_values <- as.numeric(num_parts)  # Convert to numeric
    if (any(is.na(num_values))) {
      # Handle any NA values that may result from conversion (e.g., empty strings)
      num_values <- num_values[!is.na(num_values)]
    }
    if (length(num_values) > 0) {
      data_clean$lifestyle_temps_ecran_finsemaine_travail[i] <- max(num_values, na.rm = TRUE)  # Assign the maximum value if non-empty
    } else {
      # Assign a default value or handle empty num_values vector appropriately
      data_clean$lifestyle_temps_ecran_finsemaine_travail[i] <- NA  # Or some other default or error handling
    }
  } else if (grepl("min", screen_time_str)) {
    # If "min" is found, convert from minutes to hours
    data_clean$lifestyle_temps_ecran_finsemaine_travail[i] <- as.numeric(gsub("[^0-9]", "", screen_time_str)) / 60
  } else {
    # Assume the input is in hours and just remove non-numeric characters
    data_clean$lifestyle_temps_ecran_finsemaine_travail[i] <- as.numeric(gsub("[^0-9]", "", screen_time_str))
  }
}

table(data_clean$lifestyle_temps_ecran_finsemaine_travail)

# temps__cran__3 ----------------------------------------

attributes(data_raw$temps__cran__3)
table(data_raw$temps__cran__3)
data_clean$lifestyle_temps_ecran_semaine_loisir <- NA


for (i in 1:nrow(data_raw)) {
  screen_time_str <- data_raw$temps__cran__3[i]  # Store the current value in a variable for easier handling
  
  # Clean up the string by removing all non-numeric and non-delimiter characters except delimiters
  clean_str <- gsub("[^0-9/_ -]", "", screen_time_str)
  
  if (grepl("[/_ -]", clean_str)) {
    # If there's any of the specified delimiters, split the string
    num_parts <- strsplit(clean_str, "[/_ -]")[[1]]
    num_values <- as.numeric(num_parts)  # Convert to numeric
    if (any(is.na(num_values))) {
      # Handle any NA values that may result from conversion (e.g., empty strings)
      num_values <- num_values[!is.na(num_values)]
    }
    data_clean$lifestyle_temps_ecran_semaine_loisir[i] <- max(num_values, na.rm = TRUE)  # Assign the maximum value
  } else if (grepl("min", screen_time_str)) {
    # If "min" is found, convert from minutes to hours
    data_clean$lifestyle_temps_ecran_semaine_loisir[i] <- as.numeric(gsub("[^0-9]", "", screen_time_str)) / 60
  } else {
    # Assume the input is in hours and just remove non-numeric characters
    data_clean$lifestyle_temps_ecran_semaine_loisir[i] <- as.numeric(gsub("[^0-9]", "", screen_time_str))
  }
}

table(data_clean$lifestyle_temps_ecran_semaine_loisir)  # Display the table of cleaned data


# temps__cran__4 ---------------------------------------

attributes(data_raw$temps__cran__4)
table(data_raw$temps__cran__4)
data_clean$lifestyle_temps_ecran_finsemaine_loisir <- NA

for (i in 1:nrow(data_raw)) {
  screen_time_str <- data_raw$temps__cran__4[i]  # Store the current value in a variable for easier handling
  
  # Clean up the string by removing all non-numeric and non-delimiter characters except delimiters
  clean_str <- gsub("[^0-9/_ -]", "", screen_time_str)
  
  if (grepl("[/_ -]", clean_str)) {
    # If there's any of the specified delimiters, split the string
    num_parts <- strsplit(clean_str, "[/_ -]")[[1]]
    num_values <- as.numeric(num_parts)  # Convert to numeric
    if (any(is.na(num_values))) {
      # Handle any NA values that may result from conversion (e.g., empty strings)
      num_values <- num_values[!is.na(num_values)]
    }
    if (length(num_values) > 0) {
      data_clean$lifestyle_temps_ecran_finsemaine_loisir[i] <- max(num_values, na.rm = TRUE)  # Assign the maximum value if non-empty
    } else {
      # Assign a default value or handle empty num_values vector appropriately
      data_clean$lifestyle_temps_ecran_finsemaine_loisir[i] <- NA  # Or some other default or error handling
    }
  } else if (grepl("min", screen_time_str)) {
    # If "min" is found, convert from minutes to hours
    data_clean$lifestyle_temps_ecran_finsemaine_loisir[i] <- as.numeric(gsub("[^0-9]", "", screen_time_str)) / 60
  } else {
    # Assume the input is in hours and just remove non-numeric characters
    data_clean$lifestyle_temps_ecran_finsemaine_loisir[i] <- as.numeric(gsub("[^0-9]", "", screen_time_str))
  }
}

table(data_clean$lifestyle_temps_ecran_finsemaine_loisir)


