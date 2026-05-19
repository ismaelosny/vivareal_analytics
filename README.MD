# Real Estate Market Analytics

A Python pipeline to collect, clean, and structure public data from real estate listings. It automates data extraction and saves the information into spreadsheets for financial analysis.

## Project Structure
* `src/scraper.py`: Main python script.
* `.gitignore`: Prevents pushing local data files and virtual environments to GitHub.
* `requirements.txt`: List of required Python packages.

## Tech Stack
* Python 3
* Requests
* BeautifulSoup4
* Pandas
* OpenPyXL

## How It Works
1. **Data Extraction:** Targets `application/ld+json` tags (Schema.org structured data). This keeps the script working even if the website's visual layout changes.
2. **Anti-Blocking:** Uses browser-mimicking headers and random delays (3 to 5 seconds) between requests to avoid server bans.
3. **Limit Handling:** The platform limits navigation to 50 pages per search. The script detects this server limit (Status 404) or manual stops (`Ctrl+C`) and triggers a `finally` block to save all collected data before closing.
4. **Data Cleaning:** Uses Pandas to remove duplicate listings based on property IDs and formats text and locations.

## Collected Data
The output files (CSV and Excel) include:
* `ID_Imovel` (Unique Property ID)
* `Tipo` (Property Type)
* `Bairro` (Neighborhood)
* `Preco` (Price)
* `Condominio` (HOA/Condo Fee)
* `Area_m2` (Property Size)
* `Quartos` / `Banheiros` (Bedrooms / Bathrooms)
* `Link` (Source URL)

## How to Run

1. Clone this repository:
```bash
git clone [https://github.com/ismaelosny/vivareal_analytics.git](https://github.com/ismaelosny/vivareal_analytics.git)
cd vivareal_analytics
2. Create and activate a virtual environment:
python -m venv venv
# On Windows:
venv\Scripts\activate
3. Install dependencies:
pip install -r requirements.txt
4. Run the script:
python src/scraper.py
