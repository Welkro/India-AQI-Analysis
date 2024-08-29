import pandas as pd
import lightningchart as lc

# REMOVE THE LICENSE KEY BEFORE PUBLISHING TO GITHUB
lc.set_license("LICENSE_KEY")

# Path to the CSV file containing AQI data
file_path_india = 'India_AQI.csv'

# Load the CSV file into a DataFrame
india_AQI = pd.read_csv(file_path_india)

# Use forward fill to replace null values with the last non-null value
india_AQI.ffill(inplace=True) 

# Define AQI thresholds for each pollutant
aqi_thresholds = {
    'PM2.5': {'Good': 30, 'Satisfactory': 60, 'Moderate': 90, 'Poor': 120, 'Very Poor': 250},
    'PM10': {'Good': 50, 'Satisfactory': 100, 'Moderate': 250, 'Poor': 350, 'Very Poor': 430},
    'NO2': {'Good': 40, 'Satisfactory': 80, 'Moderate': 180, 'Poor': 280, 'Very Poor': 400},
    'OZONE': {'Good': 50, 'Satisfactory': 100, 'Moderate': 168, 'Poor': 208, 'Very Poor': 748},
    'CO': {'Good': 1.0, 'Satisfactory': 2.0, 'Moderate': 10.0, 'Poor': 17.0, 'Very Poor': 34.0},
    'SO2': {'Good': 40, 'Satisfactory': 80, 'Moderate': 380, 'Poor': 800, 'Very Poor': 1600},
    'NH3': {'Good': 200, 'Satisfactory': 400, 'Moderate': 800, 'Poor': 1200, 'Very Poor': 1800}
}

# Function to map pollutant values to AQI categories
def map_to_aqi_category(value, thresholds):
    """
    Maps a pollutant value to its corresponding AQI category based on predefined thresholds.

    Parameters:
    value (float): The pollutant value.
    thresholds (dict): The thresholds for different AQI categories.

    Returns:
    str: The AQI category for the given value.
    """
    if value <= thresholds['Good']:
        return 'Good'
    elif value <= thresholds['Satisfactory']:
        return 'Satisfactory'
    elif value <= thresholds['Moderate']:
        return 'Moderate'
    elif value <= thresholds['Poor']:
        return 'Poor'
    elif value <= thresholds['Very Poor']:
        return 'Very Poor'
    else:
        return 'Severe'

# Define the color mapping for AQI categories
colors = {
    'Good': lc.Color('green'),
    'Satisfactory': lc.Color('yellowgreen'),
    'Moderate': lc.Color('yellow'),
    'Poor': lc.Color('orange'),
    'Very Poor': lc.Color('red'),
    'Severe': lc.Color('darkred')
}

# List of pollutants to create charts for
pollutants = ['PM2.5', 'PM10', 'NO2', 'OZONE', 'CO', 'SO2', 'NH3']

# Initialize the Dashboard with 4 columns and 2 rows, using a dark theme
dashboard = lc.Dashboard(columns=4, rows=2, theme=lc.Themes.Dark)

# Function to generate a chart and add it to the dashboard
def create_chart_for_dashboard(pollutant_name, column_index, row_index, row_span=1):
    """
    Generates a bar chart for the given pollutant and adds it to the dashboard.

    Parameters:
    pollutant_name (str): The name of the pollutant.
    column_index (int): The column index where the chart will be placed.
    row_index (int): The row index where the chart will be placed.
    row_span (int): The number of rows the chart should span.
    """
    # Apply the function to create a new column for AQI categories
    india_AQI[f'{pollutant_name}_AQI_Category'] = india_AQI[india_AQI['pollutant_id'] == pollutant_name]['pollutant_avg'].apply(lambda x: map_to_aqi_category(x, aqi_thresholds[pollutant_name]))

    # Count the occurrences of each AQI category
    ordered_categories = ['Good', 'Satisfactory', 'Moderate', 'Poor', 'Very Poor', 'Severe']
    aqi_counts = india_AQI[f'{pollutant_name}_AQI_Category'].value_counts().reindex(ordered_categories, fill_value=0)

    # Prepare data for the bar chart
    chart_data = [{'category': category, 'value': count} for category, count in aqi_counts.items()]

    # Create the bar chart and add it to the dashboard
    chart = dashboard.BarChart(
        vertical=True,
        column_index=column_index,
        row_index=row_index,
        row_span=row_span
    )

    chart.set_sorting('disabled')
    chart.set_data(chart_data)
    chart.set_title(f"{pollutant_name} Severity Distribution")
    chart.set_value_label_display_mode("afterBar")

    # Apply the individual colors to the bars
    for i, item in enumerate(chart_data):
        chart.set_bar_color(category=item['category'], color=colors[item['category']])

# Generate and add charts for each pollutant
create_chart_for_dashboard('PM2.5', column_index=0, row_index=0)
create_chart_for_dashboard('PM10', column_index=1, row_index=0)
create_chart_for_dashboard('NO2', column_index=2, row_index=0)
create_chart_for_dashboard('OZONE', column_index=3, row_index=0, row_span=2)  # This chart will take up two rows
create_chart_for_dashboard('CO', column_index=0, row_index=1)
create_chart_for_dashboard('SO2', column_index=1, row_index=1)
create_chart_for_dashboard('NH3', column_index=2, row_index=1)

# Open the dashboard to display the charts
dashboard.open()