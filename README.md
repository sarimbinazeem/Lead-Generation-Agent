# Lead Generation Agent

## Features

- Accepts a natural language prompt.
- Uses DigitalOcean OpenAI to extract business type and location.
- Uses Playwright to automate Bing Maps.
- Collects multiple business leads.
- Saves leads to an Excel (.xlsx) file.

## Installation

```bash
pip install -r requirements.txt
playwright install
```

## Environment Variables

Create a `.env` file:

```
DO_API_KEY=YOUR_KEY
DO_BASE_URL=YOUR_ENDPOINT
MODEL=YOUR_MODEL
```

## Run

```bash
python main.py
```

The generated Excel file will be saved in the project folder.