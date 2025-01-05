from flask import Flask, request, jsonify
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from football_scraper.queries.football_thefa import getAllData
import os, json
from football_scraper.api.contact import addFootballDataToServer
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define the route to accept an ID and trigger the Scrapy spider
@app.route('/run_spider', methods=['POST'])
def run_spider():
    try:
        # Parse JSON payload from the POST request
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400

        request_url = data.get('request_url')
        season_id = data.get('season_id')
        league_id = data.get('league_id')

        # Validate required parameters
        if not all([request_url, season_id, league_id]):
            return jsonify({"status": "error", "message": "Missing required parameters"}), 400

        # Initialize Scrapy process
        process = CrawlerProcess(get_project_settings())
        
        # Assuming your Scrapy spider is named 'thefa' and accepts these arguments
        spider_name = 'thefa'

        # Pass the parameters to the spider
        process.crawl(spider_name, request_url=request_url)
        process.start()

        # Retrieve and process data after the spider finishes
        # scraped_data = getAllData()
        # scraped_data = json.loads(json.dumps(scraped_data, default=str))
        season_id = data.get('season_id')
        league_id = data.get('league_id')
        print(season_id)
        addFootballDataToServer(league_id, season_id)
        return jsonify({
            "status": "success", 
            "message": f"Spider '{spider_name}' ran successfully."
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/')
def home():
    return "Hello, World!"

if __name__ == '__main__':
    app.run(port=5000)
