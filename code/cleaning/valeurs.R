# values_inventory
attributes(data_raw$values_inventory_1)
table(data_raw$values_inventory_1)
data_clean$valeurs_respect_elders <- sondr::finverser(data_raw$values_inventory_1 -1) / 5
table(data_clean$valeurs_respect_elders)

attributes(data_raw$values_inventory_2)
table(data_raw$values_inventory_2)
data_clean$valeurs_religiosity <- sondr::finverser(data_raw$values_inventory_2 -1) / 5
table(data_clean$valeurs_religiosity)

attributes(data_raw$values_inventory_3)
table(data_raw$values_inventory_3)
data_clean$valeurs_care_for_others <- sondr::finverser(data_raw$values_inventory_3 -1) / 5
table(data_clean$valeurs_care_for_others)

attributes(data_raw$values_inventory_4)
table(data_raw$values_inventory_4)
data_clean$attention_check_ok_2 <- NA
data_clean$attention_check_ok_2[data_raw$values_inventory_4 == 2] <- 1
data_clean$attention_check_ok_2[data_raw$values_inventory_4 != 2] <- 0
table(data_clean$attention_check_ok_2)

attributes(data_raw$values_inventory_5)
table(data_raw$values_inventory_5)
data_clean$valeurs_equal_opportunity_for_everyone <- sondr::finverser(data_raw$values_inventory_5 -1) / 5
table(data_clean$valeurs_equal_opportunity_for_everyone)

attributes(data_raw$values_inventory_6)
table(data_raw$values_inventory_6)
data_clean$valeurs_curious <- sondr::finverser(data_raw$values_inventory_6 -1) / 5
table(data_clean$valeurs_curious)

attributes(data_raw$values_inventory_7)
table(data_raw$values_inventory_7)
data_clean$valeurs_takes_risks <- sondr::finverser(data_raw$values_inventory_7 -1) / 5
table(data_clean$valeurs_takes_risks)

attributes(data_raw$values_inventory_8)
table(data_raw$values_inventory_8)
data_clean$valeurs_having_fun <- sondr::finverser(data_raw$values_inventory_8 -1) / 5
table(data_clean$valeurs_having_fun)

attributes(data_raw$values_inventory_9)
table(data_raw$values_inventory_9)
data_clean$valeurs_important_being_successful <- sondr::finverser(data_raw$values_inventory_9 -1) / 5
table(data_clean$valeurs_important_being_successful)

attributes(data_raw$values_inventory_10)
table(data_raw$values_inventory_10)
data_clean$valeurs_important_being_in_charge <- sondr::finverser(data_raw$values_inventory_10 -1) / 5
table(data_clean$valeurs_important_being_in_charge)

attributes(data_raw$values_inventory_11)
table(data_raw$values_inventory_11)
data_clean$valeurs_organized <- sondr::finverser(data_raw$values_inventory_11 -1) / 5
table(data_clean$valeurs_organized)

