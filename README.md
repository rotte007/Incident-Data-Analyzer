# cis6930fa24-project3
Data Engineering

**Name:** Rachana Rotte

## Project Description

This project involves building a web application using Flask that allows users to upload incident PDF files or provide URLs for Norman PD incident PDFs. The application extracts and processes the incident data to generate visualizations, including bar charts for the nature of incidents, time series graphs for incidents over time, and clustering visualizations based on incident locations and nature.

## How to Install
```
git clone https://github.com/rotte007/cis6930fa24-project3.git
cd cis6930fa24-project3
pip install pipenv (if not already installed)
pipenv install -e .
```

## How to Run
```
pipenv run python src/main.py

pipenv run python -m pytest -v
```
Open your web browser and navigate to:

```
http://127.0.0.1:5000/
```

![video](https://github.com/rotte007/cis6930fa24-project0/blob/main/resources/Video.gif)

## Example of Output

Example console output -> 
``` 
 * Serving Flask app 'main'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 264-523-139
127.0.0.1 - - [07/Dec/2024 18:08:29] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [07/Dec/2024 18:08:29] "GET /static/style.css HTTP/1.1" 304 -
```

## Functions

### `main.py`

- **`fetchincidents(url)`**: 
   - **Parameters**: `url` – the URL of the incident PDF.
   - **Description**: Fetches incident PDF data from a given URL.
   - **Returns**: The PDF data if successful, otherwise None.
   - **Error Handling:**: Handles HTTPError and URLError exceptions by printing the error message and returning None.

- **`extractincidents(incident_data)`**: 
   - **Parameters**: `incident_data`– the raw PDF data.
   - **Description**: Extracts incident information such as incident time, number, location, nature, and ORI from the PDF. 
   - **Returns**: A DataFrame containing the columns:incident_time, [REDACTED], incident_location, nature, incident_ori.

- **`index()`**: 
   - **Description**: Handles the file uploads and URL inputs, and redirects to the results page.
   - **HTTP Methods**: GET, POST

- **`results()`**: 
   - **HTTP Methods**: GET
   - **Description**:  Generates visualizations for the incidents, including bar charts, time series graphs, and clustering visualizations.

- **`main()`**: 
   - **Description**: Runs the Flask application in debug mode. 

### Tests

The tests for each function are located in the `tests/` folder, and they can be executed using `pytest`. Each function is tested to ensure it performs correctly with valid input, ensuring the core components work as expected.

- **`test_upload_multiple_files`**:
   - **Description**: Tests uploading multiple files and verifies the combined data.

- **`test_process_single_file`**:
   - **Description**: Tests processing a single PDF file for incident extraction.
     
- **`test_process_single_url`**:
   - **Description**: Tests processing a single URL for incident extraction.

- **`test_combined_data_visualization`**:
   - **Description**: Tests combined data visualization for multiple files and URLs.

## Approach:
1. **Data Ingestion**:
    - **File Upload**: Users can upload multiple PDF files through the web interface.
    - **URL Input**: Users can also provide multiple URLs pointing to PDF files for incident data extraction.

2. **Data Fetching and Extraction**:
    - **Fetch Incidents**: If URLs are provided, the system fetches PDF data from these URLs.
    - **Extract Incidents**: Incident data is extracted from the uploaded/fetched PDF files. The extraction includes:
        - Parsing PDF text to identify incident records.
        - Splitting lines correctly based on date-time patterns.
        - Constructing a structured DataFrame containing relevant columns like `incident_time`, `incident_number`, `incident_location`, `nature`, and `incident_ori`.

3. **Data Processing**:
    - **Datetime Conversion**: Converts `incident_time` from string format to a datetime object.
    - **Data Cleaning**: Removes records with invalid/missing datetime entries.
    - **Geocoding**: Uses Google Maps API to get latitude and longitude coordinates for incident locations.

4. **Data Visualization**:
    - **Bar Chart**: Creates a bar chart showing the frequency of different incident natures.
    - **Time Series Graphs**: Generates individual time series graphs for each uploaded/fetched PDF, displaying incident counts over time.
    - **Clustering Visualization**: 
        - Performs KMeans clustering on the geocoded incident locations.
        - Generates a scatter plot showing clusters of incidents based on location and nature, with hover tools to display the nature and time of each incident.

5. **Result Display**:
    - Combines all visualizations—bar charts, time series graphs, and clustering plots.
    - Renders these visualizations on a results page in the web interface, providing interactive visual insights into the incident data.

6. **Error Handling and User Feedback**:
    - **Error Handling**: Catches and logs errors during data fetching, extraction, and geocoding.
    - **User Notifications**: Uses flash messages to inform users about issues like failed URL fetches or upload errors.

## Bugs and Assumptions

### Bugs
- **Inconsistent PDF formatting**: If the structure of the PDF file changes, the extraction logic may fail.
- **Multiple incidents on the same line**: The script attempts to split these lines, but errors may occur if the data isn't cleanly separated.
- **Date Format**: Assumes dates in the incident PDF files follow the %m/%d/%Y %H:%M format.
- **Internet Connection**: Assumes the server running the Flask app has a stable internet connection to fetch external URLs and use the Google Maps API.
- **Google Maps API Key**: Assumes the Google Maps API key has the necessary permissions and is not restricted.

### Assumptions
- The PDFs provided by Norman PD are consistently formatted, with incident details following a similar pattern.
- Only incidents with complete information (i.e., all required fields present) are taken into consideration.
- The data is assumed to be accurate as provided by the Norman PD.
- URL Handling:URLs that do not point to valid PDF files will cause errors. HTTP errors such as 404 or 403 will be handled but result in failed URL processing.
- Date Parsing: If dates in the PDFs are not in the expected format, the parsing may fail, leading to errors in visualization generation.
- Geocoding Errors: The Google Maps API may fail to return coordinates for some locations, causing incomplete clustering data.
- Large Data Sets: Processing and visualizing very large datasets may lead to performance issues.
- Visualization Gaps: There can be gaps between the headings and graphs due to default margin settings; additional adjustments in Plotly layout settings may be required.
- Multiple Submissions: If both files and URLs are provided, the application may have difficulty managing large numbers of inputs simultaneously leading to higher runtime. 
