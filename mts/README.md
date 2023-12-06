# Multivariate Time Series
## Procedure
1. Combine the separate building dataset into one
2. Add timestamp in POSIXct format
3. Filter outliers from the dataset
    - Remove extreme data with manual thresholds
    - Removal of negative values
    - Removal of values exceeding 1.2 interquartile range (IQD)
        
        1.2 IQR was used instead of 1.5 to filter out more erroneous data and because of the sinusoidal distribution.

    - Examine the change in variability using QQ plot. The first plot represents the data before the filter. There is a large variability due to negative and large values. The second plot represents the data after the filtering. It still has a large deviation, but this is mostly due to value variation between the buildings rather than the variation within the entire dataset. 
4. Process and combine the weather data
5. Transform hourly weather data into daily
    - Mean temperature
    - Mean Humidity
    - Sum of GHI
    - HDD/CDD
6. Combine weather data with building data
7. Remove columns with no data
8. Compute Day-of-Year and Day-of-Week as integer factors
    - This models the weekly and closure date variations
9. Convert char variables into integer factors 
10. Split trainings and testing dataset
11. Conduct stepwise regression to get the most significant variables
12. Have seasonal variables as Multi-Seasonal Time Series object
13. Fit the multiple linear regression model to the stepwise model 
14. Plot forecasts against the actual with confidence intervals
15. Produce RMSE, MAR, MAPE, and R-squared values
16. Remove buildings with insufficient data
