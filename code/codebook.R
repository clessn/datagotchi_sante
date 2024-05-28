data <- haven::read_sav("_SharedFolder_datagotchi-santé/data/raw/datagotchi_sante/data_raw.sav")  %>% 
  filter(code == "complete")
codebook <- sondr::sav_to_codebook(data)

write.csv(codebook, "_SharedFolder_datagotchi-santé/data/raw/codebook.csv")
