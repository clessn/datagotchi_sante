# LatDec -----------------------------------------------------------------------
attributes(data_raw$LatDec_1)
table(data_raw$LatDec_1)
data_clean$enviro_travail_freedom_work <- sondr::finverser(data_raw$LatDec_1 -1) / 4
table(data_clean$enviro_travail_freedom_work)

attributes(data_raw$LatDec_2)
table(data_raw$LatDec_2)
data_clean$enviro_travail_influence_amount_work <- sondr::finverser(data_raw$LatDec_2 -1) / 4
table(data_clean$enviro_travail_influence_amount_work)

attributes(data_raw$LatDec_3)
table(data_raw$LatDec_3)
data_clean$enviro_travail_decide_break <- sondr::finverser(data_raw$LatDec_3 -1) / 4
table(data_clean$enviro_travail_decide_break)

attributes(data_raw$LatDec_4)
table(data_raw$LatDec_4)
data_clean$enviro_travail_influence_decisions_work <- sondr::finverser(data_raw$LatDec_4 -1) / 4
table(data_clean$enviro_travail_influence_decisions_work)

attributes(data_raw$LatDec_5)
table(data_raw$LatDec_5)
data_clean$enviro_travail_influence_do_job <- sondr::finverser(data_raw$LatDec_5 -1) / 4
table(data_clean$enviro_travail_influence_do_job)

# SoutColl ---------------------------------------------------------------------
attributes(data_raw$SoutColl_1)
table(data_raw$SoutColl_1)
data_clean$enviro_travail_colleagues_sensitive <- sondr::finverser(data_raw$SoutColl_1 -1) / 4
table(data_clean$enviro_travail_colleagues_sensitive)

attributes(data_raw$SoutColl_2)
table(data_raw$SoutColl_2)
data_clean$enviro_travail_support_from_colleagues <- sondr::finverser(data_raw$SoutColl_2 -1) / 4
table(data_clean$enviro_travail_support_from_colleagues)

attributes(data_raw$SoutColl_3)
table(data_raw$SoutColl_3)
data_clean$enviro_travail_ask_colleagues_for_help <- sondr::finverser(data_raw$SoutColl_3 -1) / 4
table(data_clean$enviro_travail_ask_colleagues_for_help)

