# drawdownraffle
## A simple Draw-Down Raffle program

You are free to use this very simple Python program to host draw-down raffles for your event. I created this program to hold draw-down raffles at my American Legion post. Drawdown raffles are a common method of fundraising for non-profits and veterans organizations.

### What it does: 
When you start the program navigate to localhost:5000 and enter the following details: First ticket number sold, Last ticket number sold, Dollar value of a ticket, and the time between draws in seconds. When you submit the information it routes you to the localhost:5000/raffle page. The program randomly draws numbers and displays the drawn and undrawn numbers. The webpage automatically refreshes every 15 seconds regardless of the draw interval. When all the numbers are drawn the last number is declared the winner and the prize dollar amount is displayed. The dollar calculation keeps 33% for the house and then rounds the prize down to the nearest dollar. The program creates a text file and appends the winning details (Date/time, Ticket Number, and Prize dollar amount) for each draw after a winner has been declared. 

### Installation:
#### Windows/Linux
1. Install python
2. Install pip
3. Install Flask and Jinja2 ``` pip install flask jinja2 ```
4. Create a directory and extract the downloaded zip file
5. create a static folder with your own logo image
6. Execute python drawdown.py

### Modification for your use:
* Change line 30 to represent your organization or event
* Change line 43 to add your logo image
* Change line 74 to include an advertising banner
* Change line 93 to reflect the percentage the house keeps (default is 33%)

This is not intended for internet use. Please ensure that this is run on your local network
