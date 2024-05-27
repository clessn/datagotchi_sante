## Taille ----------------------------------------------------------------------

attributes(data_raw$taille)
table(data_raw$taille)
attributes(data_raw$taille_1_TEXT)
table(data_raw$taille_1_TEXT)
attributes(data_raw$taille_2_TEXT)
table(data_raw$taille_2_TEXT)

data_clean$ses_taille <- NA
valid_indices_taille_1 <- which(data_raw$taille_1_TEXT != "")
valid_indices_taille_2 <- which(data_raw$taille_2_TEXT != "")
data_clean$ses_taille[valid_indices_taille_1] <- data_raw$taille_1_TEXT[valid_indices_taille_1]
data_clean$ses_taille[valid_indices_taille_2] <- data_raw$taille_2_TEXT[valid_indices_taille_2]
table(data_clean$ses_taille, useNA = "ifany")

data_clean$ses_taille_gpt <- NA

for (i in 1:nrow(data_clean)) {
  
    if (is.na(data_clean$ses_taille[i]) || data_clean$ses_taille[i] == "NA") {
      next
    } else {

    system <- "your role is to output the height of respondents in CM based on given height information" # Donne un role au modèle. Doit être clair et concis

    prompt <- paste0("Please read a survey answer representing the height of a survey respondent and convert it to centimeters. Output only a single number representing the height of the respondent in CM. The given value might be numeric or textual, might be in meters or in feet and inches. Your role is to convert the value to centimeters. Here is the respondant's height: ", data_clean$ses_taille[i]) # Ton prompt
  
    chat_prompt <- openai::create_chat_completion(
        model = "gpt-4-turbo",
        messages = list(
            list("role" = "system",
                 "content" = system
            ),
            list(
                "role" = "user",
                "content" = prompt)
            )
    )
  
  print(paste0("Taille: ", data_clean$ses_taille[i]))
  print(paste0("Taille convertie: ", chat_prompt$choices$message.content))
  Sys.sleep(1)

  data_clean$ses_taille_gpt[i] <- chat_prompt$choices$message.content

  }
}