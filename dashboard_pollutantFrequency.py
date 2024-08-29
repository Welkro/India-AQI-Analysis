import pandas as pd
import numpy as np
import lightningchart as lc

# REMOVE THE LICENSE KEY BEFORE PUBLISHING TO GITHUB
lc.set_license("LICENSE_KEY")

# Path to the CSV file containing AQI data
file_path_india = 'India_AQI.csv'

# Load the CSV file into a DataFrame
india_AQI = pd.read_csv(file_path_india)

# Use forward fill to replace null values with the last non-null value
india_AQI.ffill(inplace=True)

# Initialize a Dashboard with 3 columns and 3 rows
dashboard = lc.Dashboard(columns=3, rows=3, theme=lc.Themes.Dark)

# Define the AQI thresholds and corresponding colors for each pollutant
aqi_thresholds = {
    'PM2.5': [
        (0, 30, lc.Color('green')),  # Good
        (31, 60, lc.Color('yellowgreen')),  # Satisfactory
        (61, 90, lc.Color('yellow')),  # Moderate
        (91, 120, lc.Color('orange')),  # Poor
        (121, 250, lc.Color('red')),  # Very Poor
        (251, float('inf'), lc.Color('darkred'))  # Severe
    ],
    'PM10': [
        (0, 50, lc.Color('green')),  # Good
        (51, 100, lc.Color('yellowgreen')),  # Satisfactory
        (101, 250, lc.Color('yellow')),  # Moderate
        (251, 350, lc.Color('orange')),  # Poor
        (351, 430, lc.Color('red')),  # Very Poor
        (431, float('inf'), lc.Color('darkred'))  # Severe
    ],
    'NO2': [
        (0, 40, lc.Color('green')),  # Good
        (41, 80, lc.Color('yellowgreen')),  # Satisfactory
        (81, 180, lc.Color('yellow')),  # Moderate
        (181, 280, lc.Color('orange')),  # Poor
        (281, 400, lc.Color('red')),  # Very Poor
        (401, float('inf'), lc.Color('darkred'))  # Severe
    ],
    'OZONE': [
        (0, 50, lc.Color('green')),  # Good
        (51, 100, lc.Color('yellowgreen')),  # Satisfactory
        (101, 168, lc.Color('yellow')),  # Moderate
        (169, 208, lc.Color('orange')),  # Poor
        (209, 748, lc.Color('red')),  # Very Poor
        (749, float('inf'), lc.Color('darkred'))  # Severe
    ],
    'CO': [
        (0, 1.0, lc.Color('green')),  # Good
        (1.1, 2.0, lc.Color('yellowgreen')),  # Satisfactory
        (2.1, 10.0, lc.Color('yellow')),  # Moderate
        (10.1, 17.0, lc.Color('orange')),  # Poor
        (17.1, 34.0, lc.Color('red')),  # Very Poor
        (34.1, float('inf'), lc.Color('darkred'))  # Severe
    ],
    'SO2': [
        (0, 40, lc.Color('green')),  # Good
        (41, 80, lc.Color('yellowgreen')),  # Satisfactory
        (81, 380, lc.Color('yellow')),  # Moderate
        (381, 800, lc.Color('orange')),  # Poor
        (801, 1600, lc.Color('red')),  # Very Poor
        (1601, float('inf'), lc.Color('darkred'))  # Severe
    ],
    'NH3': [
        (0, 200, lc.Color('green')),  # Good
        (201, 400, lc.Color('yellowgreen')),  # Satisfactory
        (401, 800, lc.Color('yellow')),  # Moderate
        (801, 1200, lc.Color('orange')),  # Poor
        (1201, 1800, lc.Color('red')),  # Very Poor
        (1801, float('inf'), lc.Color('darkred'))  # Severe
    ]
}

def assign_aqi_colors(chart, bin_edges, pollutant):
    """
    Assign colors to each bin in the chart based on the AQI thresholds for the given pollutant.
    
    Parameters:
    chart (lc.Chart): The chart object to apply colors to.
    bin_edges (array): The edges of the bins used in the histogram.
    pollutant (str): The pollutant type (e.g., 'PM2.5', 'PM10').
    """
    num_bins = len(bin_edges) - 1
    thresholds = aqi_thresholds[pollutant]
    for i in range(num_bins):
        category_label = f'{bin_edges[i]:.1f} - {bin_edges[i+1]:.1f}'
        level = (bin_edges[i] + bin_edges[i+1]) / 2  # Calculate the mid-point of the bin range
        for (lower, upper, color) in thresholds:
            if lower <= level <= upper:
                chart.set_bar_color(category=category_label, color=color)
                break

# Create and configure the charts for each pollutant

# PM2.5 Chart
pollutant_data = india_AQI[india_AQI['pollutant_id'] == 'PM2.5']
y_values = pollutant_data['pollutant_avg'].tolist()
num_bins = 20
counts, bin_edges = np.histogram(y_values, bins=num_bins)
histogram_data = [{'category': f'{bin_edges[i]:.1f} - {bin_edges[i+1]:.1f}', 'value': int(counts[i])} for i in range(len(counts))]
chart_pm25 = dashboard.BarChart(column_index=0, row_index=0, column_span=2)  # Span across 2 columns
chart_pm25.set_sorting('disabled')
chart_pm25.set_data(histogram_data)
assign_aqi_colors(chart_pm25, bin_edges, 'PM2.5')
chart_pm25.set_title("Histogram of PM2.5 Levels' Frequency")

# PM10 Chart
pollutant_data = india_AQI[india_AQI['pollutant_id'] == 'PM10']
y_values = pollutant_data['pollutant_avg'].tolist()
counts, bin_edges = np.histogram(y_values, bins=num_bins)
histogram_data = [{'category': f'{bin_edges[i]:.1f} - {bin_edges[i+1]:.1f}', 'value': int(counts[i])} for i in range(len(counts))]
chart_pm10 = dashboard.BarChart(column_index=2, row_index=0)  # This will be in the third column of the first row
chart_pm10.set_sorting('disabled')
chart_pm10.set_data(histogram_data)
assign_aqi_colors(chart_pm10, bin_edges, 'PM10')
chart_pm10.set_title("Histogram of PM10 Levels' Frequency")

# NO2 Chart
pollutant_data = india_AQI[india_AQI['pollutant_id'] == 'NO2']
y_values = pollutant_data['pollutant_avg'].tolist()
counts, bin_edges = np.histogram(y_values, bins=num_bins)
histogram_data = [{'category': f'{bin_edges[i]:.1f} - {bin_edges[i+1]:.1f}', 'value': int(counts[i])} for i in range(len(counts))]
chart_no2 = dashboard.BarChart(column_index=0, row_index=1)
chart_no2.set_sorting('disabled')
chart_no2.set_data(histogram_data)
assign_aqi_colors(chart_no2, bin_edges, 'NO2')
chart_no2.set_title("Histogram of NO2 Levels' Frequency")

# NH3 Chart
pollutant_data = india_AQI[india_AQI['pollutant_id'] == 'NH3']
y_values = pollutant_data['pollutant_avg'].tolist()
counts, bin_edges = np.histogram(y_values, bins=num_bins)
histogram_data = [{'category': f'{bin_edges[i]:.1f} - {bin_edges[i+1]:.1f}', 'value': int(counts[i])} for i in range(len(counts))]
chart_nh3 = dashboard.BarChart(column_index=1, row_index=1)
chart_nh3.set_sorting('disabled')
chart_nh3.set_data(histogram_data)
assign_aqi_colors(chart_nh3, bin_edges, 'NH3')
chart_nh3.set_title("Histogram of NH3 Levels' Frequency")

# SO2 Chart
pollutant_data = india_AQI[india_AQI['pollutant_id'] == 'SO2']
y_values = pollutant_data['pollutant_avg'].tolist()
counts, bin_edges = np.histogram(y_values, bins=num_bins)
histogram_data = [{'category': f'{bin_edges[i]:.1f} - {bin_edges[i+1]:.1f}', 'value': int(counts[i])} for i in range(len(counts))]
chart_so2 = dashboard.BarChart(column_index=2, row_index=1)  # This will be in the third column of the second row
chart_so2.set_sorting('disabled')
chart_so2.set_data(histogram_data)
assign_aqi_colors(chart_so2, bin_edges, 'SO2')
chart_so2.set_title("Histogram of SO2 Levels' Frequency")

# CO Chart
pollutant_data = india_AQI[india_AQI['pollutant_id'] == 'CO']
y_values = pollutant_data['pollutant_avg'].tolist()
counts, bin_edges = np.histogram(y_values, bins=num_bins)
histogram_data = [{'category': f'{bin_edges[i]:.1f} - {bin_edges[i+1]:.1f}', 'value': int(counts[i])} for i in range(len(counts))]
chart_co = dashboard.BarChart(column_index=0, row_index=2)
chart_co.set_sorting('disabled')
chart_co.set_data(histogram_data)
assign_aqi_colors(chart_co, bin_edges, 'CO')
chart_co.set_title("Histogram of CO Levels' Frequency")

# OZONE Chart
pollutant_data = india_AQI[india_AQI['pollutant_id'] == 'OZONE']
y_values = pollutant_data['pollutant_avg'].tolist()
counts, bin_edges = np.histogram(y_values, bins=num_bins)
histogram_data = [{'category': f'{bin_edges[i]:.1f} - {bin_edges[i+1]:.1f}', 'value': int(counts[i])} for i in range(len(counts))]
chart_ozone = dashboard.BarChart(column_index=1, row_index=2, column_span=2)  # Span across 2 columns
chart_ozone.set_sorting('disabled')
chart_ozone.set_data(histogram_data)
assign_aqi_colors(chart_ozone, bin_edges, 'OZONE')
chart_ozone.set_title("Histogram of OZONE Levels' Frequency")

# Open the dashboard to display the charts
dashboard.open()