from flask import Flask, request, render_template, redirect, url_for, flash
import urllib.request
import io
import re
import pandas as pd
import plotly.express as px
import plotly.io as pio
from sklearn.cluster import KMeans
from pypdf import PdfReader
import googlemaps

app = Flask(__name__, template_folder='resources', static_folder='static')
app.secret_key = 'supersecretkey'
gmaps = googlemaps.Client(key='AIzaSyDwVap1b7kGdntm8hK_0JG7idWfvJ5jOTE')

incidents_df_list = []  # List to hold dataframes from multiple files or URLs

def fetch_incidents(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    req = urllib.request.Request(url, headers=headers)
    try:
        pdf_data = urllib.request.urlopen(req).read()
        return pdf_data
    except urllib.error.HTTPError as e:
        print(f"HTTPError: {e.code} - {e.reason}")
        return None
    except urllib.error.URLError as e:
        print(f"URLError: {e.reason}")
        return None

def extract_incidents(incident_data):
    incidents = []
    with io.BytesIO(incident_data) as file:
        pdf_reader = PdfReader(file)
        num_pages = len(pdf_reader.pages)
        s = ""
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            s += page.extract_text(extraction_mode="layout")
        lines = s.split("\n")[3:-1]
        lines = [line for line in lines if line.strip()]
        date_pattern = r'\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2}'
        split_lines = []
        for line in lines:
            date_pointers = [match.start() for match in re.finditer(date_pattern, line)]
            if len(date_pointers) > 1:
                split_lines.append(line[date_pointers[0]:date_pointers[1] - 1])
                split_lines.append(line[date_pointers[1]:])
            else:
                split_lines.append(line)
        incidents_dict = []
        for line in split_lines:
            k = line.split("    ")
            k = [item for item in k if item]
            if len(k) == 5:
                incidents_dict.append({
                    'incident_time': k[0].strip(),
                    'incident_number': k[1].strip(),
                    'incident_location': k[2].strip(),
                    'nature': k[3].strip(),
                    'incident_ori': k[4].strip()
                })
    return pd.DataFrame(incidents_dict)

@app.route('/', methods=['GET', 'POST'])
def index():
    global incidents_df_list
    incidents_df_list = []
    if request.method == 'POST':
        if 'files' in request.files:
            files = request.files.getlist('files')
            for file in files:
                if file and file.filename != '':
                    incident_data = file.read()
                    df = extract_incidents(incident_data)
                    incidents_df_list.append(df)
        if 'urls' in request.form:
            urls = request.form.getlist('urls')
            for url in urls:
                if url:
                    incident_data = fetch_incidents(url)
                    if incident_data:
                        df = extract_incidents(incident_data)
                        incidents_df_list.append(df)
                    else:
                        flash("Failed to retrieve the PDF file from the provided URL. Please check the URL and try again.")
    
        if incidents_df_list:
            return redirect(url_for('results'))
    return render_template('index.html')

@app.route('/results')
def results():
    global incidents_df_list
    if not incidents_df_list:
        return "No data available"

    combined_df = pd.concat(incidents_df_list)

    # Convert 'incident_time' to datetime
    try:
        combined_df['incident_time'] = pd.to_datetime(combined_df['incident_time'], errors='coerce', format='%m/%d/%Y %H:%M')
    except Exception as e:
        print(f"Date parsing exception: {e}")

    cleaned_df = combined_df.dropna(subset=['incident_time'])

    # Visualization 1: Bar chart of Nature vs Frequency
    nature_counts = cleaned_df['nature'].value_counts().reset_index()
    nature_counts.columns = ['Nature', 'Count']
    fig_bar = px.bar(nature_counts, x='Nature', y='Count', title='Incident Nature Counts')
    fig_bar.update_layout(margin=dict(l=20, r=20, t=40, b=20))

    bar_chart = pio.to_html(fig_bar, full_html=False, include_plotlyjs='cdn')

    # Visualization 2: Time series line graph for each file/date
    time_series_charts = []
    for df in incidents_df_list:
        df['incident_time'] = pd.to_datetime(df['incident_time'], errors='coerce', format='%m/%d/%Y %H:%M')
        df['time'] = df['incident_time'].dt.time
        df_cleaned = df.dropna(subset=['incident_time'])
        date = df_cleaned['incident_time'].dt.date.unique()[0]
        time_series_data = df_cleaned.groupby('time').size().reset_index(name='Count')
        fig_time_series = px.line(time_series_data, x='time', y='Count', title=f'Time Series of Incident Count by Time of the Day ({date})')
        fig_time_series.update_layout(margin=dict(l=20, r=20, t=40, b=20))
        time_series_chart = pio.to_html(fig_time_series, full_html=False, include_plotlyjs='cdn')
        time_series_charts.append(time_series_chart)

    # Visualization 3: Clustering based on Location and Nature
    locations = cleaned_df['incident_location'].dropna().unique()
    location_coords = []
    for loc in locations:
        try:
            geocode_result = gmaps.geocode(loc)
            if geocode_result:
                latlng = geocode_result[0]['geometry']['location']
                location_coords.append((loc, latlng['lat'], latlng['lng']))
        except Exception as e:
            print(f"Geocoding error: {e}")

    location_df = pd.DataFrame(location_coords, columns=['location', 'lat', 'lng'])
    if not location_df.empty:
        cluster_df = cleaned_df.merge(location_df, left_on='incident_location', right_on='location')
        if len(cluster_df) > 0:
            kmeans = KMeans(n_clusters=3)
            clusters = kmeans.fit_predict(cluster_df[['lat', 'lng']])
            cluster_df['Cluster'] = clusters
            fig_cluster = px.scatter(cluster_df, x='lng', y='lat', color='Cluster', title='Clustering of Incidents Based on Location and Nature',
                                     hover_data=['nature', 'incident_time'])
            fig_cluster.update_layout(margin=dict(l=20, r=20, t=40, b=20))

            cluster_chart = pio.to_html(fig_cluster, full_html=False, include_plotlyjs='cdn')
        else:
            cluster_chart = None
    else:
        cluster_chart = None

    return render_template('results.html', bar_chart=bar_chart, time_series_charts=time_series_charts, cluster_chart=cluster_chart)

if __name__ == '__main__':
    app.run(debug=True)
