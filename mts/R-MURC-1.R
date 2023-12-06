library(tidyverse)
library(dplyr)
library(fasttime)
library(lubridate)
library(tseries)
library(forecast)
library(GGally)
library(broom)
library(visdat)
library(StepReg)
library(forcats)
# Define path
path <- "../Usage Data/_edit_collection"

# Get a list of files in the directory
files <- list.files(path)

# Empty DataFrame
EUI_All <- read.csv("../R/Timestamp.csv")
Buildings <- list()
EUI_Combined <- data.frame()

# Loop through each file in the directory
for (file in files) {
  # Check if the file ends with 'csv'
  if (endsWith(file, ".csv")) {
    # Create the file path
    file_path <- file.path(path, file)
    
    # Split the file name using '_' as a separator
    parts <- unlist(strsplit(file, "_"))
    
    # Extract the name (assuming it's the second element after splitting)
    name <- parts[2]
    Buildings <- append(Buildings, name)
    
    # Read the CSV file and store it in the 'csv_list' using the name as the key
    assign(name, read.csv(file_path))
    
    # Combine all
    EUI_Combined <- rbind(EUI_Combined, data.frame(assign(name, read.csv(file_path)), 
                                          rep(name, nrow(read.csv(file_path)))))
      
  }
}

# Add timestamp
EUI_Combined <- EUI_Combined %>%
  mutate(Timestamp = fastPOSIXct(Timestamp) + days(1))
names(EUI_Combined)[46] <- "Building"


# Filter for outliers, round 1
EUI_Combined2 <- EUI_Combined %>%
  mutate(Total_EUI_excwtr = ifelse(Total_EUI_excwtr > 70, NA, Total_EUI_excwtr)) %>%
  mutate(Thrm_Energy = ifelse(Thrm_Energy > 100000, NA, Thrm_Energy)) %>%
  mutate(Thrm_Power = ifelse(Thrm_Energy > 100000, NA, Thrm_Power)) %>%
  mutate(Wtr_Cns = ifelse(Wtr_Cns > 100000, NA, Wtr_Cns)) %>%
  mutate(Elec_EUI = ifelse(Elec_EUI > 10000, NA, Elec_EUI)) %>%
  mutate(Thrm_EUI = ifelse(Thrm_EUI > 100, NA, Thrm_EUI)) %>%
  mutate(Wtr_WUI = ifelse(Wtr_WUI > 10, NA, Wtr_WUI)) %>%
  mutate(Elec_Energy = ifelse(Elec_Energy > 20000, NA, Elec_Energy)) %>%
  mutate(Wtr_WUI = ifelse(Wtr_WUI > 4000, NA, Wtr_WUI)) %>%
  mutate(Date = date(Timestamp))

# Check for outliers
ggplot(EUI_Combined2, aes(sample = Total_EUI_excwtr)) +
  geom_qq()

Outlier1sigma <- EUI_Combined2 %>%
  select(BLDG_UID, Total_EUI_excwtr, Thrm_Energy, Wtr_Cns, Elec_EUI, Thrm_EUI, Wtr_WUI, Elec_Energy) %>%
  group_by(BLDG_UID) %>%
  summarize_all(sd, na.rm = TRUE)

Outlier1sigma

OutlierIQR <- EUI_Combined2 %>%
  select(BLDG_UID, Total_EUI_excwtr, Thrm_Energy, Wtr_Cns, Elec_EUI, Thrm_EUI, Wtr_WUI, Elec_Energy) %>%
  group_by(BLDG_UID) %>%
  summarize_all(quantile, na.rm = TRUE)

view(OutlierIQR)

# Filter for outliers, round 2, negative
EUI_Combined3 <- EUI_Combined2 %>%
  group_by(BLDG_UID) %>%
  mutate(Total_EUI_excwtr = ifelse(Total_EUI_excwtr < 0, NA, Total_EUI_excwtr)) %>%
  mutate(Thrm_Energy = ifelse(Thrm_Energy < 0, NA, Thrm_Energy)) %>%
  mutate(Thrm_Power = ifelse(Thrm_Energy < 0, NA, Thrm_Power)) %>%
  mutate(Wtr_Cns = ifelse(Wtr_Cns < 0, NA, Wtr_Cns)) %>%
  mutate(Elec_EUI = ifelse(Elec_EUI < 0, NA, Elec_EUI)) %>%
  mutate(Thrm_EUI = ifelse(Thrm_EUI < 0, NA, Thrm_EUI)) %>%
  mutate(Wtr_WUI = ifelse(Wtr_WUI < 0, NA, Wtr_WUI)) %>%
  mutate(Elec_Energy = ifelse(Elec_Energy < 0, NA, Elec_Energy)) %>%
  mutate(Elec_Power = ifelse(Elec_Power < 0, NA, Elec_Power))



# Filter for outliers, round 2, by 1.2IQR and above
EUI_Combined4 <- EUI_Combined3 %>%
  group_by(BLDG_UID) %>%
  mutate(Total_EUI_excwtr = ifelse(Total_EUI_excwtr > (median(na.omit(Total_EUI_excwtr)) + 1.2 * IQR(na.omit(Total_EUI_excwtr))), NA, Total_EUI_excwtr)) %>%
  mutate(Thrm_Energy = ifelse(Thrm_Energy > (median(na.omit(Thrm_Energy)) + 1.2 * IQR(na.omit(Thrm_Energy))), NA, Thrm_Energy)) %>%
  mutate(Thrm_Power = ifelse(Thrm_Power > (median(na.omit(Thrm_Power)) + 1.2 * IQR(na.omit(Thrm_Power))), NA, Thrm_Power)) %>%
  mutate(Wtr_Cns = ifelse(Wtr_Cns > (median(na.omit(Wtr_Cns)) + 1.2 * IQR(na.omit(Wtr_Cns))), NA, Wtr_Cns)) %>%
  mutate(Elec_EUI = ifelse(Elec_EUI > (median(na.omit(Elec_EUI)) + 1.2 * IQR(na.omit(Elec_EUI))), NA, Elec_EUI)) %>%
  mutate(Thrm_EUI = ifelse(Thrm_EUI > (median(na.omit(Thrm_EUI)) + 1.2 * IQR(na.omit(Thrm_EUI))), NA, Thrm_EUI)) %>%
  mutate(Wtr_WUI = ifelse(Wtr_WUI > (median(na.omit(Wtr_WUI)) + 1.2 * IQR(na.omit(Wtr_WUI))), NA, Wtr_WUI)) %>%
  mutate(Elec_Energy = ifelse(Elec_Energy > (median(na.omit(Elec_Energy)) + 1.2 * IQR(na.omit(Elec_Energy))), NA, Elec_Energy)) %>%
  mutate(Elec_Power = ifelse(Elec_Power > (median(na.omit(Elec_Power)) + 1.2 * IQR(na.omit(Elec_Power))), NA, Elec_Power)) %>%
  mutate(Wtr_Cns = ifelse(Wtr_Cns > (median(na.omit(Wtr_Cns)) + 1.2 * IQR(na.omit(Wtr_Cns))), NA, Wtr_Cns))
  


# Filter for outliers, round 2, by 1.5IQR and above (IGNORE)
EUI_Combined5 <- EUI_Combined3 %>%
  group_by(BLDG_UID) %>%
  mutate(Total_EUI_excwtr = ifelse(Total_EUI_excwtr < (median(na.omit(Total_EUI_excwtr)) + 1.5 * IQR(na.omit(Total_EUI_excwtr))), NA, Total_EUI_excwtr)) %>%
  mutate(Thrm_Energy = ifelse(Thrm_Energy < (median(na.omit(Thrm_Energy)) + 1.5 * IQR(na.omit(Thrm_Energy))), NA, Thrm_Energy)) %>%
  mutate(Thrm_Power = ifelse(Thrm_Power < (median(na.omit(Thrm_Power)) + 1.5 * IQR(na.omit(Thrm_Power))), NA, Thrm_Power)) %>%
  mutate(Wtr_Cns = ifelse(Wtr_Cns < (median(na.omit(Wtr_Cns)) + 1.5 * IQR(na.omit(Wtr_Cns))), NA, Wtr_Cns)) %>%
  mutate(Elec_EUI = ifelse(Elec_EUI < (median(na.omit(Elec_EUI)) + 1.5 * IQR(na.omit(Elec_EUI))), NA, Elec_EUI)) %>%
  mutate(Thrm_EUI = ifelse(Thrm_EUI < (median(na.omit(Thrm_EUI)) + 1.5 * IQR(na.omit(Thrm_EUI))), NA, Thrm_EUI)) %>%
  mutate(Wtr_WUI = ifelse(Wtr_WUI < (median(na.omit(Wtr_WUI)) + 1.5 * IQR(na.omit(Wtr_WUI))), NA, Wtr_WUI)) %>%
  mutate(Elec_Energy = ifelse(Elec_Energy < (median(na.omit(Elec_Energy)) + 1.5 * IQR(na.omit(Elec_Energy))), NA, Elec_Energy))

# Check again
ggplot(EUI_Combined4, aes(sample = Total_EUI_excwtr)) +
  geom_qq()

ggplot(EUI_Combined4, aes(x = Total_EUI_excwtr)) +
  geom_histogram(bins = 40)

ggplot(EUI_Combined5, aes(sample = Total_EUI_excwtr)) +
  geom_qq()

ggplot(EUI_Combined5, aes(x = Total_EUI_excwtr)) +
  geom_histogram(bins = 40)

EUI_Outlier <- EUI_Combined4 %>%
  filter(Total_EUI_excwtr > 10) %>%
  select(Total_EUI_excwtr, Building)

ggplot(EUI_Outlier, aes(y=Building)) +
  geom_bar()

# Import weather data
Weather <- read.csv("../Weather Data/YVR_psm3-2-2_60_2012-2021.csv")

# Calculate heating/cooling degree days
base_temp <- 18

# To POSIX
Weather <- Weather %>% 
  mutate(Datetime = as.POSIXct(paste(Weather$Year, Weather$Month, Weather$Day, Weather$Hour, sep = " "),
                               format = "%Y %m %d %H"
  ))

# Calculate Mean Temp
Avg_Temp_Daily <- Weather %>%
  mutate(Date = date(Datetime)) %>%
  group_by(Date) %>%
  summarise(Avg_Temp_Daily = mean(Temperature)) %>%
  filter(!is.na(Date))

# Calculate HDD
HDD_Daily <- Weather %>%
  mutate(HDD_hourly = pmax(0, base_temp - Temperature)) %>%
  mutate(Date = date(Datetime)) %>%
  group_by(Date) %>%
  summarise(HDD_daily = sum(HDD_hourly) / 24) %>%
  filter(!is.na(Date))

# Calculate CDD
CDD_Daily <- Weather %>%
  mutate(CDD_hourly = pmax(0, Temperature - base_temp)) %>%
  mutate(Date = date(Datetime)) %>%
  group_by(Date) %>%
  summarise(CDD_daily = sum(CDD_hourly) / 24) %>%
  filter(!is.na(Date))

# Calculate Daily GHI sum
GHI_Daily <- Weather %>%
  mutate(Date = date(Datetime)) %>%
  group_by(Date) %>%
  summarise(GHI_sum = sum(GHI)) %>%
  filter(!is.na(Date))

# Calculate Daily average humidity
Humidity_Daily <- Weather %>%
  mutate(Date = date(Datetime)) %>%
  group_by(Date) %>%
  summarise(Humidity_avg = sum(Relative.Humidity) / 24) %>%
  filter(!is.na(Date))

# Join into one DataFrame
Weather_Daily <- HDD_Daily %>%
  inner_join(CDD_Daily, by = "Date") %>%
  inner_join(GHI_Daily, by = "Date") %>%
  inner_join(Avg_Temp_Daily, by = "Date") %>%
  inner_join(Humidity_Daily, by = "Date")

# Join to weather file
EUI_Weather <- EUI_Combined4 %>%
  right_join(Weather_Daily, by = "Date")

view(EUI_Weather)

# Variable selection
EUI_Weather2 <- EUI_Weather %>%
  select(BLDG_UID, Building:Humidity_avg, Elec_Power:GBA) %>%
  select(-Elec_ConF, -Thrm_ConF, -Wtr_ConF) %>%
  mutate(DayOfYear = yday(Date)) %>%
  mutate(DayOfWeek = as.factor(wday(Date)))

view(EUI_Weather2)

# As factor
EUI_Weather3 <- EUI_Weather2 %>%
  mutate(BLDG_UID = as.factor(BLDG_UID)) %>%
  mutate(Building = as.factor(Building)) %>%
  mutate(Constr_Type = as.factor(Constr_Type)) %>%
  mutate(Condition = as.factor(Condition))
  
summary(EUI_Weather3)

# Missing data visualization
EUI_Miss <- EUI_Weather3 %>%
  summarise(across(everything(), ~ sum(is.na(.)))) %>%
  select_if(is.numeric) %>%
  map_dbl(sum)

view(EUI_Miss)

# Model
EUI_Weather4 <- EUI_Weather3 %>%
  select(Building:Humidity_avg, Total_EUI_excwtr:DayOfYear, -Green_Status, DayOfWeek)

EUI_Weather4$Condition <- fct_explicit_na(EUI_Weather4$Condition)

view(EUI_Weather4)
# Pairplot
EUI_Brief <- EUI_Weather4 %>%
  ungroup(BLDG_UID) %>%
  select(-BLDG_UID, -Building, -Date)
  # %>%
  # ggpairs()

# Regular linear regression
model_all <- lm(Total_EUI_excwtr ~ ., data = EUI_Brief)
summary(model_all)

# Train test split
EUI_Train <- EUI_Weather4 %>%
  filter(Date > "2012-01-01") %>%
  filter(Date < "2020-01-01")
EUI_Train <- EUI_Train[!(is.na(EUI_Train$Total_EUI_excwtr)), ]

view(EUI_Train)

EUI_Test = EUI_Weather4 %>%
  filter(Date > "2020-01-01")
view(EUI_Test)

# Stepwise regression
both <- stepwise(data = EUI_Brief, selection = "bidirection", formula = Total_EUI_excwtr ~ 
                   DayOfYear + 
                   HDD_daily +
                   CDD_daily +
                   GHI_sum +
                   Avg_Temp_Daily +
                   Humidity_avg +
                   Occu_Date +
                   MAX_Floors + FSP_Classroom + FSP_Lab + FSP_Library +
                   FSP_Office + BLDG_Height + GFA + GBA, select = "AIC")

both$`Coefficients of the Selected Variables`
both$`Selected Varaibles`

forward <- stepwise(data = EUI_Brief, selection = "bidirection", formula = Total_EUI_excwtr ~ 
                   DayOfYear + 
                   HDD_daily +
                   CDD_daily +
                   GHI_sum +
                   Avg_Temp_Daily +
                   Humidity_avg +
                   Occu_Date +
                   MAX_Floors + FSP_Classroom + FSP_Lab + FSP_Library +
                   FSP_Office + BLDG_Height + GFA + GBA, select = "AIC")

forward$`Coefficients of the Selected Variables`
forward$`Selected Varaibles`

# Time series regression
# Define msts objects
tDoY <- msts(EUI_Train$DayOfYear, seasonal.periods = 365)
tDoW <- msts(EUI_Train$DayOfWeek, seasonal.periods = 7)
tHDD <- msts(EUI_Train$HDD_daily, seasonal.periods = 365)
tCDD <- msts(EUI_Train$CDD_daily, seasonal.periods = 365)
tGHI <- msts(EUI_Train$GHI_sum, seasonal.periods = 365)
tTEM <- msts(EUI_Train$Avg_Temp_Daily, seasonal.periods = 365)
tHUM <- msts(EUI_Train$Humidity_avg, seasonal.periods = 365)
tEUI <- msts(EUI_Train$Total_EUI_excwtr, seasonal.periods = c(7, 365))

# Model fit
view(EUI_Train)
TSLMfit <- tslm(data = EUI_Train, tEUI ~ DayOfYear + DayOfWeek +
                  tHDD +
                  tCDD +
                  tGHI +
                  tHUM +
                  Occu_Date + Constr_Type + Condition +
                  MAX_Floors + FSP_Classroom + FSP_Lab + FSP_Library +
                  FSP_Office + BLDG_Height + GFA + GBA)

summary(TSLMfit)

# Updated model
TSLMfit2 <- tslm(data = EUI_Train, tEUI ~ DayOfWeek +
                  tHDD +
                  tCDD +
                  tGHI +
                  tHUM +
                  Occu_Date + Constr_Type + Condition +
                  MAX_Floors + FSP_Classroom + FSP_Lab + FSP_Library +
                  FSP_Office + BLDG_Height + GFA + GBA)

summary(TSLMfit2)

stats <- data.frame()
# Building model function

building_fun <- function(building) {
  n <- date_decimal
  
  # Train model
  training_data <- EUI_Train %>%
    filter(Building == building)
  
  tDoY2 <- msts(training_data$DayOfYear, seasonal.periods = 365)
  tDoW2 <- msts(training_data$DayOfWeek, seasonal.periods = 7)
  tHDD2 <- msts(training_data$HDD_daily, seasonal.periods = 365)
  tCDD2 <- msts(training_data$CDD_daily, seasonal.periods = 365)
  tGHI2 <- msts(training_data$GHI_sum, seasonal.periods = 365)
  tTEM2 <- msts(training_data$Avg_Temp_Daily, seasonal.periods = 365)
  tHUM2 <- msts(training_data$Humidity_avg, seasonal.periods = 365)
  tEUI2 <- msts(training_data$Total_EUI_excwtr, seasonal.periods = c(7, 365))
  
  TSLMBuilding <- tslm(data = training_data, formula = tEUI2 ~ 
                         DayOfWeek +
                         tHDD2 +
                         tCDD2 +
                         tGHI2 +
                         tHUM2)
  
  TSLMBuilding
    
  building_data <- EUI_Test %>%
    filter(Building == building) %>%
    replace(is.na(.), 0)
    # mutate(Elapsed = (as.integer(Date) - 18263) / 365.25 + date_decimal(first(Date)) - 2020)
  
  fDOY <- msts(building_data$DayOfYear, seasonal.periods = 365)
  fHDD <- msts(building_data$HDD_daily, seasonal.periods = 365)
  fCDD <- msts(building_data$CDD_daily, seasonal.periods = 365)
  fGHI <- msts(building_data$GHI_sum, seasonal.periods = 365)
  fTEM <- msts(building_data$Avg_Temp_Daily, seasonal.periods = 365)
  fHUM <- msts(building_data$Humidity_avg, seasonal.periods = 365)
  fEUI <- msts(building_data$Total_EUI_excwtr, seasonal.periods = c(7, 365))

  Forecast_Horizon <- building_data %>% 
    data.frame(
    Date = building_data$Date,
    tDoY2 = fDOY,
    tEUI2 = rep(NA, 729),
    tHDD2 = fHDD,
    tCDD2 = fCDD,
    tGHI2 = fGHI,
    tTEM2 = fTEM,
    tHUM2 = fHUM)
  
  TSLMforecastBuilding <- forecast(TSLMBuilding, newdata = Forecast_Horizon, h = 1)
  return(TSLMforecastBuilding)
}

# Forecast all
building_all_fun <- function(test_data) {
  n <- date_decimal
  
  building_data <- test_data %>%
    replace(is.na(.), 0)
    # mutate(Elapsed = (as.integer(Date) - 18263) / 365.25 + date_decimal(first(Date)) - 2020)
  
  fDOY <- msts(building_data$DayOfYear, seasonal.periods = 365)
  fHDD <- msts(building_data$HDD_daily, seasonal.periods = 365)
  fCDD <- msts(building_data$CDD_daily, seasonal.periods = 365)
  fGHI <- msts(building_data$GHI_sum, seasonal.periods = 365)
  fTEM <- msts(building_data$Avg_Temp_Daily, seasonal.periods = 365)
  fHUM <- msts(building_data$Humidity_avg, seasonal.periods = 365)
  fEUI <- msts(building_data$Total_EUI_excwtr, seasonal.periods = c(7, 365))
  
  Forecast_Horizon <- building_data %>% 
    data.frame(
      Date = building_data$Date,
      tDoY = fDOY,
      tEUI = rep(NA, 729),
      tHDD = fHDD,
      tCDD = fCDD,
      tGHI = fGHI,
      tTEM = fTEM,
      tHUM = fHUM)

  TSLMforecastAll <- forecast(TSLMfit2, newdata = Forecast_Horizon, h = 1)
  
  return(TSLMforecastAll)
}

# Forecast for all
TSLMforecastAll <- building_all_fun(test_data = EUI_Test)



# Plot forecasts
building_plot_fun <- function(building, model) {
  historical_data <- EUI_Train %>%
    filter(Building == building) %>%
    mutate(EUI_History = Total_EUI_excwtr)

  verif_data <- EUI_Test %>%
    filter(Building == building) %>%
    mutate(EUI_Verif = Total_EUI_excwtr)
  
  forecast_data <- data.frame(
    EUI_Forecast = model$mean,
    EUI_High = model$upper,
    EUI_Low = model$lower,
    Date = c(seq.Date(ymd('2020-01-02'), ymd('2020-02-28'), by = '1 day'), seq.Date(ymd('2020-03-01'), ymd('2021-12-31'), by = '1 day'))
  )

  plot_data <- historical_data %>%
    full_join(verif_data) %>%
    full_join(forecast_data) %>%
    select(Date, EUI_History, EUI_Verif, EUI_Forecast, EUI_High.1, EUI_Low.1, EUI_High.2, EUI_Low.2)
    
  plot <- ggplot(plot_data) +
    geom_line(aes(x = Date, y = EUI_History)) +
    geom_ribbon(aes(x = Date, ymin = EUI_Low.2, ymax = EUI_High.2), fill = "lightblue", alpha = 0.2) +
    geom_ribbon(aes(x = Date, ymin = EUI_Low.1, ymax = EUI_High.1), fill = "mediumblue", alpha = 0.2) +
    geom_line(aes(x = Date, y = EUI_Forecast), color = "darkblue") +
    geom_line(aes(x = Date, y = EUI_Verif), color = "red") +
    ggtitle(building)
  
  return(plot)
}

# Testing and validation
# Verification
building_stat_fun <- function(building, model) {
  historical_data <- EUI_Train %>%
    filter(Building == building) %>%
    mutate(EUI_History = Total_EUI_excwtr)
  
  verif_data <- EUI_Test %>%
    filter(Building == building) %>%
    mutate(EUI_Verif = Total_EUI_excwtr)
  
  forecast_data <- data.frame(
    EUI_Forecast = model$mean,
    EUI_High = model$upper,
    EUI_Low = model$lower,
    Date = c(seq.Date(ymd('2020-01-02'), ymd('2020-02-28'), by = '1 day'), seq.Date(ymd('2020-03-01'), ymd('2021-12-31'), by = '1 day'))
  )
  
  plot_data <- historical_data %>%
    full_join(verif_data) %>%
    full_join(forecast_data) %>%
    select(Date, EUI_History, EUI_Verif, EUI_Forecast, EUI_High.1, EUI_Low.1, EUI_High.2, EUI_Low.2)
  
  observed <- as.vector(plot_data$EUI_Verif)
  forecasted <- as.vector(plot_data$EUI_Forecast)
  
  resid <- na.omit(observed - forecasted)
  resid
  # Calculate RMSE
  rmse <- sqrt(mean((resid)^2))
  
  # Calculate MAE
  mae <- mean(abs(resid))
  
  # Calculate MAPE
  mape <- mean(abs((resid) / na.omit(observed))) * 100
  
  # Calculate R-squared (R^2)
  ssr <- sum((resid)^2)  # Sum of squared residuals
  sst <- sum((na.omit(observed) - mean(na.omit(observed)))^2)  # Total sum of squares
  rsquared <- 1 - (ssr / sst)
  
  stats <- c(rmse, mae, mape, rsquared)
  return(stats)
}

# INSERT BUILDING HERE
TSLMforecastBuilding <- building_fun(building = "AERL")
plot <- building_plot_fun(building = "AERL", model = TSLMforecastBuilding)
plot

stat <- building_stat_fun(building = "AERL", model = TSLMforecastBuilding)
stat

autoplot(TSLMforecastBuilding)
summary(TSLMforecastBuilding)

stats <- data.frame(
  Building = character(),
  RSME = numeric(),
  MAE = numeric(),
  MAPE = numeric(),
  Rsquared = numeric(),
  stringsAsFactors = FALSE
)

indices_to_remove <- c(-5, -16, -17, -36, -47, -54, -55, -56, -64, -65)
Buildings_filtered <- Buildings[indices_to_remove]

# Generate forecasts for all
for (building in Buildings_filtered) {
  TSLMIter <- building_fun(building = building)
  plot <- building_plot_fun(building = building, model = TSLMIter)
  stat <- building_stat_fun(building = building, model = TSLMIter)
  stats[nrow(stats) + 1,] = c(building, stat)
  
  plot_name <- paste(building, ".png", sep = "")
  png(plot_name, width = 1920, height = 1080)
  print(plot)
  dev.off()
}
