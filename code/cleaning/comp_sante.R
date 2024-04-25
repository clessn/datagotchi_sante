# comp_sante

# I focus my attention on the present moment
table(data_raw$autogestion_1)
attributes(data_raw$autogestion_1)
data_clean$comp_sante_focus_attention_present <- sondr::clean_likert_numeric_vector(data_raw$autogestion_1)
table(data_clean$comp_sante_focus_attention_present)

# I am learning to live with my strengths and weaknesses.
table(data_raw$autogestion_2)
attributes(data_raw$autogestion_2)
data_clean$comp_sante_learn_live_strengths_weaknesses <- sondr::clean_likert_numeric_vector(data_raw$autogestion_2)
table(data_clean$comp_sante_learn_live_strengths_weaknesses)

# I congratulate myself on my successes, big and small
table(data_raw$autogestion_3)
attributes(data_raw$autogestion_3)
data_clean$comp_sante_congratulate_myself_successes <- sondr::clean_likert_numeric_vector(data_raw$autogestion_3)
table(data_clean$comp_sante_congratulate_myself_successes)

# I try to love myself as I am.
table(data_raw$autogestion_4)
attributes(data_raw$autogestion_4)
data_clean$comp_sante_try_love_myself_as_i_am <- sondr::clean_likert_numeric_vector(data_raw$autogestion_4)
table(data_clean$comp_sante_try_love_myself_as_i_am)

# I consider my abilities when I make my schedule.
table(data_raw$autogestion_5)
attributes(data_raw$autogestion_5)
data_clean$comp_sante_consider_abilities_make_schedule <- sondr::clean_likert_numeric_vector(data_raw$autogestion_5)
table(data_clean$comp_sante_consider_abilities_make_schedule)

# I consider my abilities when I make my schedule.
table(data_raw$autogestion_6)
attributes(data_raw$autogestion_6)
data_clean$comp_sante_consider_abilities_make_schedule <- sondr::clean_likert_numeric_vector(data_raw$autogestion_6)
table(data_clean$comp_sante_consider_abilities_make_schedule)


