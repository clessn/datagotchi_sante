data <- haven::read_sav("_SharedFolder_datagotchi-santé/data/raw/Datagotchi-Santé_Pilote_May 21, 2024_11.55.sav")
codebook <- sondr::sav_to_codebook(data)

write.csv(codebook, "_SharedFolder_datagotchi-santé/data/raw/codebook.csv")
