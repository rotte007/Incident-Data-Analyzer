import os
import sys
import unittest
from flask import Flask

# Add the `src` directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from main import app, extract_incidents

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_upload_multiple_files(self):
        """
        Test uploading multiple files and verify the combined data is correct.
        """
        test_files = [
            'src/tests/test_file1.pdf',
            'src/tests/test_file2.pdf'
        ]

        data = {
            'files': [(open(file, 'rb')) for file in test_files]
        }
        
        response = self.app.post('/', content_type='multipart/form-data', data=data)

        # Check if the response is a redirect (to show success)
        self.assertEqual(response.status_code, 302)

        # Follow the redirect to the results page
        response = self.app.get('/results')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Incident Data Visualizations', response.get_data(as_text=True))

    def test_process_single_file(self):
        """
        Test processing a single PDF file for incident extraction.
        """
        with open('src/tests/test_file1.pdf', 'rb') as pdf:
            incidents_df = extract_incidents(pdf.read())
            self.assertFalse(incidents_df.empty)
            self.assertIn('incident_time', incidents_df.columns)
            self.assertIn('incident_number', incidents_df.columns)

    def test_process_single_url(self):
        """
        Test processing a single URL for incident extraction.
        """
        # Ensure this URL points to an accessible PDF file for your test
        test_url = 'https://www.normanok.gov/sites/default/files/documents/2024-12/2024-11-30_daily_incident_summary.pdf'
        response = self.app.post('/', data={'urls': [test_url]})
        
        # Check if the response is a redirect (Since the URL may not be accessible, this error is expected)
        self.assertEqual(response.status_code, 302)

        # Follow the redirect to the results page
        response = self.app.get('/results')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Incident Data Visualizations', response.get_data(as_text=True))

    def test_combined_data_visualization(self):
        """
        Test combined data visualization for multiple files and URLs.
        """
        with open('src/tests/test_file1.pdf', 'rb') as pdf1, open('src/tests/test_file2.pdf', 'rb') as pdf2:
            data = {
                'files': [pdf1, pdf2],
                'urls': ['https://www.normanok.gov/sites/default/files/documents/2024-12/2024-11-30_daily_incident_summary.pdf']          }
            response = self.app.post('/', content_type='multipart/form-data', data=data)

            # Check if the response is a redirect (to show success)
            self.assertEqual(response.status_code, 302)

            # Follow the redirect to the results page
            response = self.app.get('/results')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Incident Data Visualizations', response.get_data(as_text=True))

if __name__ == "__main__":
    unittest.main()
