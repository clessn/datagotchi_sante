data <- haven::read_sav("~/Dropbox/git/datagotchi_sante/_SharedFolder_datagotchi-santé/data/raw/data_raw.sav")

codebook <- sondr::sav_to_codebook(data)

write.csv(codebook, "~/Dropbox/git/datagotchi_sante/_SharedFolder_datagotchi-santé/data/raw/raw_codebook.csv")
