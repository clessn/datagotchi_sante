###############
# Packages
###############

# packages installation for the first time only
install.packages("readr")
install.packages("dotenv")
install.packages("lubridate")
install.packages("psych") 
install.packages("corrr") 
install.packages("tidyverse")
install.packages("Rnest")
install.packages("purrr")
install.packages("broom")
install.packages("emmeans")


# packages loading
library(readr) # reading csv files
library(dotenv) # loading environment variables from .env file
library(lubridate) # for date manipulation
library(tidyverse) # for data wrangling
library(emmeans) # for post-hoc tests

###############
# Loading data
###############

# load .env file
load_dot_env(".env")

# read path from environment variable
data_result_path <- Sys.getenv("DATA_RESULT_PATH")

# build the path to the file with results
clean_results_file_path <-
  file.path(data_result_path, "clean", "clean_results.csv")

# read file
clean_results <- read_csv(clean_results_file_path)

# convert columns to appropriate types
# duration, remove date part and convert to duration
clean_results$study_duration <-
  hms(sub(".* ", "", clean_results$study_duration))

# factor
cols_to_factor <- c(
  "explain_type",
  "sociodemo_01",
  "sociodemo_02",
  "sociodemo_03",
  "sociodemo_05",
  "sociodemo_07",
  "sociodemo_08"
)

clean_results[cols_to_factor] <-
  lapply(clean_results[cols_to_factor], as.factor)

# show the head of the data
head(clean_results)
sapply(clean_results, class)

###############
# Reorder/recategorize factor variables
###############

# Gender
table(clean_results$sociodemo_01) # Keeping only women/men

wrang_results <- clean_results %>%
  mutate(
    sociodemo_01 = case_when(
      sociodemo_01 == "Female (cisgender female)" ~ "Female",
      sociodemo_01 == "Male (cisgender male)" ~ "Male",
      TRUE ~ NA_character_
    ),
    sociodemo_01 = factor(sociodemo_01, levels = c("Female", "Male"))
  )

# Country
wrang_results <- wrang_results %>%
  mutate(sociodemo_02 = ifelse(sociodemo_02 == "Yes", "Born Canada", "Not born Canada"),
         sociodemo_02 = factor(sociodemo_02,
                               levels = c("Born Canada",
                                          "Not born Canada")))

# Children
wrang_results <- wrang_results %>%
  mutate(
    sociodemo_05 = ifelse(sociodemo_05 == "0", "0", "1 or more children"),
    sociodemo_05 = factor(sociodemo_05, level = c("0", "1 or more children"))
  )

# Income 
wrang_results <- wrang_results %>% 
  mutate(sociodemo_07 = case_when(
    sociodemo_07 %in% c("No income",
                        "$1 to $30,000",
                        "$30,001 to $60,000") ~ "60k and below",
    sociodemo_07 %in% c("$60,001 to $90,000",
                        "$90,001 to $110,000") ~ "60k-110k",
    sociodemo_07 == "$110,001 to $150,000" ~ "110k-150k",
    sociodemo_07 %in% c("$150,001 to $200,000",
                        "More than $200,000") ~ "150k+"),
    
    sociodemo_07 = factor(sociodemo_07,
                          levels = c("60k and below",
                                     "60k-110k",
                                     "110k-150k",
                                     "150k+")))

# Education
wrang_results <- wrang_results %>% 
  mutate(sociodemo_08 = case_when(
    sociodemo_08 %in% c("High school", "Elementary school") ~ "High school or less",
    sociodemo_08 == "College, CEGEP, or Classical College" ~ "College, CEGEP, or Classical College",
    sociodemo_08 %in% c("Bachelor's degree", "Master's degree", "PhD") ~ "University"),
    sociodemo_08 = factor(sociodemo_08,
                          levels = c("High school or less",
                                     "College, CEGEP, or Classical College",
                                     "University")))
# Age
wrang_results <- wrang_results %>% 
  rename(age = sociodemo_09)

# Prediction error
wrang_results <- wrang_results %>%
  mutate(prediction_error_wellbeing_score = abs(predicted_wellbeing_score - observed_wellbeing_score))

###############
# Manipulation checks
###############

# Manipulation model for visual
manip_model_visual <-
  lm(manipulation_visual ~ relevel(explain_type, ref = "explain_visual"),
     data = wrang_results)

summary(manip_model_visual)

# Manipulation model for textual
manip_model_textual <-
  lm(manipulation_textual ~ relevel(explain_type, ref = "explain_textual"),
     data = wrang_results)

summary(manip_model_textual)

# Manipulation model for quantitative
manip_model_quantitative <-
  lm(
    manipulation_quantitative ~ relevel(explain_type, ref = "explain_quantitative"),
    data = wrang_results)

summary(manip_model_quantitative)

# Manipulation model for interactive
manip_model_interactive <-
  lm(manipulation_interactive ~ relevel(explain_type, ref = "explain_interactive"),
     data = wrang_results)

summary(manip_model_interactive)

# Manipulation model for contextual
manip_model_contextual <-
  lm(manipulation_contextual ~ relevel(explain_type, ref = "explain_contextual"),
     data = wrang_results)

summary(manip_model_contextual)

###############
# Psychometric exploration
###############
library(psych) # For EFA
library(corrr) # For nice correlations matrix/heatmap
library(tidyverse)

# Correlation analysis
wrang_results %>%
  select(contains("importance") | contains("intention")) %>%
  correlate() %>%
  shave() %>%
  fashion()

# Reliability estimate
importance_intention_vars <- wrang_results %>%
  select(contains("importance") | contains("intention"))

alpha(importance_intention_vars)

# Factorial structure (EFA)

# Nb. of factors
library(Rnest) # To estimate the optimal number of factors to retain in the EFA

rnest_res <- nest(importance_intention_vars)
rnest_res

summary(rnest_res)
plot(rnest_res)

# As expected, we obtain lots of factor. This comes from the strong correlations
# between intention and importance for each domain. This is known as method effect.
# We need to create a composite score for intention and importance before doing EFA.

# Composite score exploration

# 1. Raw sum
wrang_results <- wrang_results %>%
  mutate(
    sum_sleep = importance_sleep + intention_sleep,
    sum_diet  = importance_diet  + intention_diet,
    sum_social = importance_social + intention_social,
    sum_neigh = importance_neighborhood + intention_neighborhood,
    sum_vol   = importance_volunteering + intention_volunteering
  )

# Correlation analysis
wrang_results %>%
  select(starts_with("sum")) %>%
  correlate() %>%
  shave() %>%
  fashion()

# Reliability estimate
sum_scores <- wrang_results %>%
  select(starts_with("sum"))

alpha(sum_scores)

# Factorial structure (EFA)

# Nb. of factors
rnest_res_sum <- nest(sum_scores)
rnest_res_sum

summary(rnest_res_sum) # Suggesting 2 factors

# EFA
efa_sum <-
  fa(
    sum_scores,
    nfactors = 2,
    rotate = "oblimin",
    fm = "minres",
    alpha = .05,
    use = "pairwise",
    warning = TRUE
  )

efa_sum # The solution reveals a social dimension and an health dimension

# 2. Weighted sum (importance > intention)
# More weight is on importance here (in line with intrinsic motivation)

w_imp <- 0.65
w_int <- 0.35

wrang_results <- wrang_results %>%
  mutate(
    w_sum_sleep = w_imp * importance_sleep + w_int * intention_sleep,
    w_sum_diet  = w_imp * importance_diet  + w_int * intention_diet,
    w_sum_social = w_imp * importance_social + w_int * intention_social,
    w_sum_neigh = w_imp * importance_neighborhood + w_int * intention_neighborhood,
    w_sum_vol   = w_imp * importance_volunteering + w_int * intention_volunteering
  )

# Correlation analysis
wrang_results %>%
  select(starts_with("w_sum")) %>%
  correlate() %>%
  shave() %>%
  fashion()

# Reliability estimate
w_sum_scores <- wrang_results %>%
  select(starts_with("w_sum"))

alpha(w_sum_scores)

# Factorial structure (EFA)

# Nb. of factors
rnest_res_sum <- nest(w_sum_scores)
rnest_res_sum

summary(rnest_res_sum) # Suggesting 2 factors

# EFA
efa_w_sum <-
  fa(
    w_sum_scores,
    nfactors = 2,
    rotate = "oblimin",
    fm = "minres",
    alpha = .05,
    use = "pairwise",
    warning = TRUE
  )

efa_w_sum # The solution reveals a social dimension and an health dimension

# Computing the composite scores (both weighted and raw)
wrang_results <- wrang_results %>%
  mutate(
    health_intent_sum = sum_sleep + sum_diet,
    social_intent_sum = sum_social + sum_neigh + sum_vol,
    intent_sum = health_intent_sum + social_intent_sum,
    health_intent_weight_sum = w_sum_sleep + w_sum_diet,
    social_intent_weigth_sum = w_sum_social + w_sum_neigh + w_sum_vol,
    intent_weight_sum = health_intent_weight_sum + social_intent_weigth_sum
  )

###############
# Main models
###############
library(purrr) # to iterate across a vector in a function

lm_FUN <- function(DV, data, socio_pattern = "socio") {
  socio_vec <- data %>%
    dplyr::select(dplyr::contains(socio_pattern), age) %>%
    select(-sociodemo_03) %>% 
    names()
  
  if (DV == "knowledge_after_score") {
    lm_formula <- reformulate(c("knowledge_before_score",
                                "explain_type",
                                "prediction_error_wellbeing_score",
                                "observed_wellbeing_score",
                                socio_vec),
                              response = DV)  
  } else{
    lm_formula <- reformulate(c(
                                "explain_type",
                                "prediction_error_wellbeing_score",
                                "observed_wellbeing_score",
                                socio_vec),
                              response = DV)  
  }
  
  
  lm(lm_formula, data = data)
}

# Vector of VDs
vd_vec <- c("health_intent_sum",
            "social_intent_sum",
            #"health_intent_weight_sum",
            #"social_intent_weigth_sum",
            "intent_sum",
            #"intent_weight_sum",
            "knowledge_after_score",
            "satisfaction_score")

lm_outputs <- map(vd_vec, ~ lm_FUN(.x, wrang_results))

names(lm_outputs) <- vd_vec

lm_outputs

# For clean results
library(broom)

add_sigstars <- function(tbl) {
  tbl %>%
    mutate(
      sig = case_when(
        p.value < 0.001 ~ "***",
        p.value < 0.01  ~ "**",
        p.value < 0.05  ~ "*",
        p.value < 0.1   ~ ".",
        TRUE            ~ ""
      )
    )
}

clean_lm_output <- map(lm_outputs, ~ broom::tidy(.x) %>% 
                         add_sigstars())
clean_lm_output
