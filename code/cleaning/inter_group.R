# know_eng_1

attributes(data_raw$know_eng_1)
table(data_raw$know_eng_1)
attributes(data_raw$know_eng_1_TEXT)
table(data_raw$know_eng_1_TEXT)
data_clean$know_english_media_personality <- NA
data_clean$know_english_media_personality <- data_raw$know_eng_1_TEXT
data_clean$know_english_media_personality[data_clean$know_english_media_personality == ""] <- "don't know"
table(data_clean$know_english_media_personality)

# know_eng_2

attributes(data_raw$know_eng_2)
table(data_raw$know_eng_2)
attributes(data_raw$know_eng_2_TEXT)
table(data_raw$know_eng_2_TEXT)
data_clean$know_english_singer <- NA
data_clean$know_english_singer <- data_raw$know_eng_2_TEXT
data_clean$know_english_singer[data_clean$know_english_singer == ""] <- "don't know"
table(data_clean$know_english_singer)

# know_eng_3

attributes(data_raw$know_eng_3)
table(data_raw$know_eng_3)
attributes(data_raw$know_eng_3_TEXT)
table(data_raw$know_eng_3_TEXT)
data_clean$know_english_actor <- NA
data_clean$know_english_actor <- data_raw$know_eng_3_TEXT
data_clean$know_english_actor[data_clean$know_english_actor == ""] <- "don't know"
table(data_clean$know_english_actor)

# know_eng_4

attributes(data_raw$know_eng_4)
table(data_raw$know_eng_4)
attributes(data_raw$know_eng_4_TEXT)
table(data_raw$know_eng_4_TEXT)
data_clean$know_english_writer <- NA
data_clean$know_english_writer <- data_raw$know_eng_4_TEXT
data_clean$know_english_writer[data_clean$know_english_writer == ""] <- "don't know"
table(data_clean$know_english_writer)

# friends_1

attributes(data_raw$friends_1)
table(data_raw$friends_1)
data_clean$french_speaking_friends <- NA
data_clean$french_speaking_friends[data_raw$friends_1 == 1] <- "1_2"
data_clean$french_speaking_friends[data_raw$friends_1 == 2] <- "3_4"
data_clean$french_speaking_friends[data_raw$friends_1 == 3] <- "5_6"
data_clean$french_speaking_friends[data_raw$friends_1 == 4] <- "7+"
data_clean$french_speaking_friends <- factor(data_clean$french_speaking_friends, levels = c("1_2", "3_4", "5_6", "7+"))
table(data_clean$french_speaking_friends)

# friends_2

attributes(data_raw$friends_2)
table(data_raw$friends_2)
data_clean$english_speaking_friends <- NA
data_clean$english_speaking_friends[data_raw$friends_2 == 1] <- "1_2"
data_clean$english_speaking_friends[data_raw$friends_2 == 2] <- "3_4"
data_clean$english_speaking_friends[data_raw$friends_2 == 3] <- "5_6"
data_clean$english_speaking_friends[data_raw$friends_2 == 4] <- "7+"
data_clean$english_speaking_friends <- factor(data_clean$english_speaking_friends, levels = c("1_2", "3_4", "5_6", "7+"))
table(data_clean$english_speaking_friends)

# friends_3

attributes(data_raw$friends_3)
table(data_raw$friends_3)
data_clean$other_language_speaking_friends <- NA
data_clean$other_language_speaking_friends[data_raw$friends_3 == 1] <- "1_2"
data_clean$other_language_speaking_friends[data_raw$friends_3 == 2] <- "3_4"
data_clean$other_language_speaking_friends[data_raw$friends_3 == 3] <- "5_6"
data_clean$other_language_speaking_friends[data_raw$friends_3 == 4] <- "7+"
data_clean$other_language_speaking_friends <- factor(data_clean$other_language_speaking_friends, levels = c("1_2", "3_4", "5_6", "7+"))
table(data_clean$other_language_speaking_friends)

# ling_1

attributes(data_raw$ling_1)
table(data_raw$ling_1)
data_clean$french_speaking_skills <- NA
data_clean$french_speaking_skills <- data_raw$ling_1 / 10
table(data_clean$french_speaking_skills)

# ling_2

attributes(data_raw$ling_2)
table(data_raw$ling_2)
data_clean$english_speaking_skills <- NA
data_clean$english_speaking_skills <- data_raw$ling_2 / 10
table(data_clean$english_speaking_skills)
