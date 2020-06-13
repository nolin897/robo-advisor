# robo-advisor

I) PROJECT SETUP

1) Create a new repo called robo-advisor with a Readme.md file and a Python .gitignore file, as well as a license of your choosing.

2) Clone the repo to your Github desktop suite

3) Create a sub-folder calld "app" within the "robo-advisor" folder and create a file called "robo_advisor.py" in this "app" folder.

4) Copy and paste the following into "robo_advisor.py":

        # app/robo_advisor.py

        print("-------------------------")
        print("SELECTED SYMBOL: XYZ")
        print("-------------------------")
        print("REQUESTING STOCK MARKET DATA...")
        print("REQUEST AT: 2018-02-20 02:00pm")
        print("-------------------------")
        print("LATEST DAY: 2018-02-20")
        print("LATEST CLOSE: $100,000.00")
        print("RECENT HIGH: $101,000.00")
        print("RECENT LOW: $99,000.00")
        print("-------------------------")
        print("RECOMMENDATION: BUY!")
        print("RECOMMENDATION REASON: TODO")
        print("-------------------------")
        print("HAPPY INVESTING!")
        print("-------------------------")

5) Create a file called "requirements.txt" in the "robo-advisor" folder and enter the following package information:

        requests
        python-dotenv

6) Set up a virtual environment:

        conda create -n stocks-env python=3.7 # (first time only)
        conda activate stocks-env

7) Install the requirements via your requirements.txt file:

        pip install -r requirements.txt

8) Run the python script via the apps folder:

        python app/robo_advisor.py

9) Set up a .env file with your secret API key set equal to the environment variable named ALPHAVANTAGE_API_KEY     

10) Install Requests package via pip