library(tidyverse)
library(dplyr)
library(fasttime)
library(lubridate)
library(tseries)
library(forecast)
library(GGally)
options(viewer.max.print = 10000)

# Define path
path <- "../Usage Data/_edit_collection"

# Get a list of files in the directory
files <- list.files(path)

# Empty DataFrame
EUI_All <- read.csv("./Timestamp.csv")
Buildings <- list()

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
  }
}

view(Buildings)
AERL <- read.csv("../Usage Data/_edit_collection/_AERL_edit.csv")

# Exploratory
AERL2 <- AERL %>%
  mutate(Timestamp = fastPOSIXct(Timestamp) + days(1))

ggplot(AERL, aes(x = Total_EUI_excwtr)) +
  geom_histogram()

ggplot(`Alumni Centre`, aes(x = Total_EUI_excwtr)) +
  geom_boxplot()

# Filter for outliers
AERL2 <- AERL2 %>%
  mutate(Total_EUI_excwtr = ifelse(Total_EUI_excwtr > 10, NA, Total_EUI_excwtr)) %>%
  mutate(Thrm_Energy = ifelse(Thrm_Energy > 10000, NA, Thrm_Energy)) %>%
  mutate(Thrm_Power = ifelse(Thrm_Energy > 10000, NA, Thrm_Power)) %>%
  mutate(Wtr_Cns = ifelse(Wtr_Cns > 10000, NA, Wtr_Cns)) %>%
  mutate(Elec_EUI = ifelse(Elec_EUI > 1000, NA, Elec_EUI)) %>%
  mutate(Thrm_EUI = ifelse(Thrm_EUI > 10, NA, Thrm_EUI)) %>%
  mutate(Wtr_WUI = ifelse(Wtr_WUI > 1, NA, Wtr_WUI)) %>%
  mutate(Elec_Energy = ifelse(Elec_Energy > 2000, NA, Elec_Energy)) %>%
  mutate(Date = date(Timestamp))

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

# Export daily weather as csv
write.csv(Weather_Daily, file = "./YVR Daily Weather 2012-2021.csv", row.names = FALSE)

# Join to weather file
AERL_Weather <- AERL2 %>%
  right_join(Weather_Daily, by = "Date")

# Plots
ggplot(AERL_Weather, aes(x = Date, y = Elec_Energy)) +
  geom_line()
ggplot(AERL_Weather, aes(x = Date, y = Elec_Power)) +
  geom_line()
ggplot(AERL_Weather, aes(x = Date, y = Thrm_Energy)) +
  geom_line()
ggplot(AERL_Weather, aes(x = Date, y = Thrm_Power)) +
  geom_line()
ggplot(AERL_Weather, aes(x = Date, y = Wtr_Cns)) +
  geom_line()

# Train/test split
AERL_Train = AERL_Weather[1652:2382, ]
AERL_Train <- AERL_Train[!(is.na(AERL_Train$Total_EUI_excwtr)), ]
AERL_Train <- AERL_Train %>%
  mutate(DayOfYear = yday(Date))
view(AERL_Train)
AERL_Test = AERL_Weather[2383:3650, ]
AERL_Test <- AERL_Test %>%
  mutate(Elapsed = (as.integer(Date) - 17724) / 365 + 3) %>%
  mutate(DayOfYear = yday(Date))
view(AERL_Test)

#Set msts objects
tDoY <- msts(AERL_Train$DayOfYear, seasonal.periods = 365)
tHDD <- msts(AERL_Train$HDD_daily, seasonal.periods = 365)
tCDD <- msts(AERL_Train$CDD_daily, seasonal.periods = 365)
tGHI <- msts(AERL_Train$GHI_sum, seasonal.periods = 365)
tHUM <- msts(AERL_Train$Humidity_avg, seasonal.periods = 365)
tELE <- msts(AERL_Train$Elec_Energy, seasonal.periods = c(7, 365))
tTHE <- msts(AERL_Train$Thrm_Energy, seasonal.periods = c(7, 365))
tWTR <- msts(AERL_Train$Wtr_Cns, seasonal.periods = c(7, 365))
tEUI <- msts(AERL_Train$Total_EUI_excwtr, seasonal.periods = c(7, 365))

# Fit to model (Dynamic Harmonic Regression)
DHRfit <- tslm(data = AERL_Train, tEUI ~ DayOfYear +
              fourier(tHDD, K = 3) +
              fourier(tCDD, K = 3) +
              fourier(tGHI, K = 3) +
              fourier(tHUM, K = 3) +
              fourier(tELE, K = c(3, 10)) +
              fourier(tTHE, K = c(3, 10)) +
              fourier(tWTR, K = c(3, 10)))
summary(DHRfit)

TSLMfit <- tslm(data = AERL_Train, tEUI ~ DayOfYear +
                 tHDD +
                 tCDD +
                 tGHI +
                 tHUM)
summary(TSLMfit)
# Define forecast horizon
fDoY <- msts(AERL_Test$DayOfYear, seasonal.periods = 365)
fHDD <- msts(AERL_Test$HDD_daily, seasonal.periods = 365)
fCDD <- msts(AERL_Test$CDD_daily, seasonal.periods = 365)
fGHI <- msts(AERL_Test$GHI_sum, seasonal.periods = 365)
fHUM <- msts(AERL_Test$Humidity_avg, seasonal.periods = 365)
fELE <- msts(AERL_Test$Elec_Energy, seasonal.periods = c(7, 365))
fTHE <- msts(AERL_Test$Thrm_Energy, seasonal.periods = c(7, 365))
fWTR <- msts(AERL_Test$Wtr_Cns, seasonal.periods = c(7, 365))
fEUI <- msts(AERL_Test$Total_EUI_excwtr, seasonal.periods = c(7, 365))

# Forecast_Horizon <- data.frame(
#   Date = AERL_Test$Date,
#   DayOfYear = AERL_Test$DayOfYear,
#   tHDD = fourier(fHDD, K = 3),
#   tCDD = fourier(fCDD, K = 3),
#   tGHI = fourier(fGHI, K = 3),
#   tHUM = fourier(fHUM, K = 3),
#   tELE = fourier(fELE, K = c(3, 10)),
#   tTHE = fourier(fTHE, K = c(3, 10)),
#   tWTR = fourier(fWTR, K = c(3, 10)),
#   tEUI = rep(NA, 1268)
# )

Forecast_Horizon <- data.frame(
  Date = AERL_Test$Date,
  DayOfYear = AERL_Test$DayOfYear,
  tHDD = fHDD,
  tCDD = fCDD,
  tGHI = fGHI,
  tHUM = fHUM,
  tEUI = rep(NA, 1268)
)
view(Forecast_Horizon)
# Forecast
TSLMforecast <- forecast(TSLMfit, newdata = Forecast_Horizon, h = 1)
view(TSLMforecast)

# Plot forecasts
autoplot <- autoplot(TSLMforecast)
autoplot

verifplot <- autoplot + geom_line(data = AERL_Test, aes(y = Total_EUI_excwtr, x = Elapsed), color = "red")
verifplot

# Verification
observed <- as.vector(AERL_Test$Total_EUI_excwtr)
forecasted <- as.vector(TSLMforecast$mean)
view(observed)
view(forecasted)

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
stats

stats_model0 <- c(0.06838291, 0.04936862, 15.19078035, 0.84269991)
stats_model1_weather_only <- c(0.09822000, 0.07644462, 29.68658793, 0.67548585)
stats_model2_transformed <- c(0.09918012, 0.07862069, 29.85990168, 0.66911044)

# Correlation Plots
AERL_Brief <- data.frame(
  DayOfYear = yday(AERL_Weather$Date),
  fDayOfYear = fourier(msts(yday(AERL_Weather$Date), seasonal.periods = 365), K = 1),
  HDD = AERL_Weather$HDD_daily,
  CDD = AERL_Weather$CDD_daily,
  GHI = AERL_Weather$GHI_sum,
  Humidity = AERL_Weather$Humidity_avg,
  EUI = AERL_Weather$Total_EUI_excwtr
)

ggpairs(AERL_Brief)


# Transformed Day of Year
TSLMfit2 <- tslm(data = AERL_Train, tEUI ~ 
                  tDoY +
                  Temp_Deseasonalized +
                  tHDD +
                  tCDD +
                  tGHI +
                  tHUM)

Forecast_Horizon2 <- data.frame(
    Date = AERL_Test$Date,
    tDoY = fDoY,
    tTEM = AERL_Test$Temp_Deseasonalized,
    tHDD = fHDD,
    tCDD = fCDD,
    tGHI = fGHI,
    tHUM = fHUM,
    tEUI = rep(NA, 1268)
)

TSLMforecast2 <- forecast(TSLMfit2, newdata = Forecast_Horizon2, h = 1)
autoplot2 <- autoplot(TSLMforecast2)
autoplot2

verifplot2 <- autoplot2 + geom_line(data = AERL_Test, aes(y = Total_EUI_excwtr, x = Elapsed), color = "red")
verifplot2

forecasted2 <- as.vector(TSLMforecast2$mean)
resid2 <- na.omit(observed - forecasted2)

# Calculate RMSE
rmse2 <- sqrt(mean((resid2)^2))

# Calculate MAE
mae2 <- mean(abs(resid2))

# Calculate MAPE
mape2 <- mean(abs((resid2) / na.omit(observed))) * 100

# Calculate R-squared (R^2)
ssr2 <- sum((resid2)^2)  # Sum of squared residuals
sst <- sum((na.omit(observed) - mean(na.omit(observed)))^2)  # Total sum of squares
rsquared2 <- 1 - (ssr2 / sst)

stats2 <- c(rmse2, mae2, mape2, rsquared2)
stats2

# Sinusoidal transform
# Fit the sine wave equation to your data
sinetrans <- nls(Avg_Temp_Daily ~ A*sin(omega*yday(Date) + phi) + C, data = AERL_Weather, start = list(A = 1, omega = 1, phi = 1, C = 1))

# Extract the coefficients
coeff <- coef(fit)

# Create a time series object from the temperature data
tTEM <- ts(AERL_Weather$Avg_Temp_Daily, frequency = 365)

# Decompose the time series into its components
tDecomp <- decompose(tTEM)

# Subtract the seasonal component from the original temperature data
Temp_Deseasonalized <- tTEM - tDecomp$seasonal

AERL_Weather <- data.frame(AERL_Weather, Temp_Deseasonalized)

# Plot result
ggplot(AERL_Weather, aes(x=yday(Date), y=Temp_Deseasonalized)) + 
  geom_point()

#### RETURN TO LINE 139, THEN 267