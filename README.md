# Data Plotter

Data Plotter is a small FastAPI web app that lets you upload a CSV file, clean the numeric data, and generate a Plotly chart from it.

## Features

- Upload a CSV file from the browser
- Automatically clean the dataset by removing missing and non-numeric columns
- Generate charts such as scatter, line, bar, and 3D plots
- View basic column statistics alongside the graph

## Tech Stack

- FastAPI
- Jinja2
- Pandas
- Plotly
- Uvicorn

## Dependencies

- fastapi==0.104.1
- uvicorn==0.24.0
- pandas==2.1.3
- plotly==5.18.0
- python-multipart==0.0.6
- Jinja2==3.1.2


## Running the App

Start the server with:

```bash
python main.py
```

Then open:

```text
http://127.0.0.1:8000/
```

## Usage

1. Open the homepage
2. Upload a CSV file
3. Choose a plot type
4. Submit the form to view the generated graph

## Project Structure

- main.py - FastAPI app entry point
- frontend/ - HTML templates and static assets
- services/ - data cleaning and plotting logic
- uploads/ - sample uploaded files
