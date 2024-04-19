data <- haven::read_sav("_SharedFolder_datagotchi-santé/data/raw/Datagotchi-Santé_Pilote_April 3, 2024_09.12.sav")

codebook <- sondr::sav_to_codebook(data)

write.csv(codebook, "_SharedFolder_datagotchi-santé/data/raw/codebook.csv")
