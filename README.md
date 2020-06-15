# robo-advisor

TO RUN THE ROBO ADVISOR:

NB: The following steps assume you have cloned this repo to your Github desktop suite from https://github.com/nolin897/robo-advisor

1) Set up a .env file in your cloned repo with your secret API key set equal to the environment variable ALPHAVANTAGE_API_KEY that is referenced in the script. If you haven't already, get your secret API key from https://www.alphavantage.co/support/#api-key    

2) Set up a virtual environment:

        conda create -n stocks-env python=3.7 # (first time only)
        conda activate stocks-env

3) Install the package requirements via the requirements.txt file:

        pip install -r requirements.txt

4) Run the script via apps/robo_advisor.py

5) Enter desired stock symbols and enter "DONE" or "done" when finished.

6) Receive investment recommendations based on the following rule:

    BUY if the stock's price increases more than 100 bps from the previous close.
    SELL if the stocks's price decreases more than 100 bps from the previous close.
    HOLD if the stock's price remains within 100 bps of the previous close.

7) For additional analysis, consult the time series that this script generates via Plotly, or view the raw data on each of the csv files created for your selected stocks. These csv files will populate in the data subfolder of this repo.    