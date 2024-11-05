from flask import Flask, render_template_string, request, redirect, url_for
from threading import Timer
import random
from datetime import datetime
import math  # Import math module for rounding down

app = Flask(__name__)

# Initial variables
ticket_numbers = []
draw_interval = 15
current_draw_index = -1  # Start with no tickets drawn
drawn_numbers = []  # List to store drawn numbers
raffle_details = {
    "start_ticket": None,
    "end_ticket": None,
    "ticket_price": None,
    "winning_amount": None,
    "winner": None
}

# HTML Template with Jinja2
raffle_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="15">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>American Legion Post ## Draw-Down Raffle</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        h1 { color: darkblue; font-size: 2em; margin-top: 0; }
        .winner { color: red; font-size: 2em; }
        .banner { margin-top: 50px; }
        .logo { width: 100px; margin-bottom: 20px; }
        .numbers { font-size: 1.5em; }
        .drawn { color: red; }
        .undrawn { color: blue; }
    </style>
</head>
<body>
    <img src="{{ url_for('static', filename='al.jpg') }}" alt="American Legion Logo" class="logo">
    <h1>American Legion Post ## Draw-Down Raffle</h1>
    
    {% if not raffle_details.winner %}
        <h2>Current Draw: {{ ticket_numbers[current_draw_index] if current_draw_index >= 0 and current_draw_index < len(ticket_numbers) else "Pending..." }}</h2>
        <h3>All Drawn Numbers:</h3>
        <div class="numbers">
            {% for number in drawn_numbers %}
                <span class="drawn">{{ number }}</span> 
            {% endfor %}
        </div>
        <h3>Remaining Tickets:</h3>
        <div class="numbers">
            {% for number in ticket_numbers %}
                {% if number not in drawn_numbers %}
                    <span class="undrawn">{{ number }}</span> 
                {% endif %}
            {% endfor %}
        </div>
    {% else %}
        <h2 class="winner">Winner: Ticket {{ raffle_details.winner }}</h2>
        <h2>Winning Amount: ${{ raffle_details.winning_amount }}</h2>
        <h3>All Drawn Numbers:</h3>
        <div class="numbers">
            {% for number in drawn_numbers %}
                <span class="drawn">{{ number }}</span> 
            {% endfor %}
        </div>
    {% endif %}
    
    <div class="banner">
        <img src="{{ url_for('static', filename='banner.jpg') }}" alt="Ad Banner">
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def setup_raffle():
    global raffle_details, ticket_numbers, current_draw_index, drawn_numbers, draw_interval  # Declare all globals at the start

    if request.method == "POST":
        # Gather inputs from the form
        start_ticket = int(request.form["start_ticket"])
        end_ticket = int(request.form["end_ticket"])
        ticket_price = float(request.form["ticket_price"])
        draw_interval = int(request.form["draw_interval"])
        
        # Calculate the winning amount with 33% house retention, rounded down
        total_pot = (end_ticket - start_ticket + 1) * ticket_price
        winning_amount = total_pot * (1 - 0.33)
        raffle_details["winning_amount"] = math.floor(winning_amount)  # Round down to nearest dollar

        # Initialize raffle details
        raffle_details["start_ticket"] = start_ticket
        raffle_details["end_ticket"] = end_ticket
        raffle_details["ticket_price"] = ticket_price
        raffle_details["winner"] = None

        # Generate list of ticket numbers
        ticket_numbers = list(range(start_ticket, end_ticket + 1))
        current_draw_index = -1  # Reset to start with no tickets drawn
        drawn_numbers = []  # Reset drawn numbers list

        # Start the draw process
        start_draws()

        return redirect(url_for("raffle_page"))
    
    return """
    <h1>Raffle Setup</h1>
    <form method="post">
        <label>Start Ticket Number:</label><br>
        <input type="number" name="start_ticket" required><br><br>
        
        <label>End Ticket Number:</label><br>
        <input type="number" name="end_ticket" required><br><br>
        
        <label>Ticket Price (in dollars):</label><br>
        <input type="number" step="0.01" name="ticket_price" required><br><br>
        
        <label>Draw Interval (seconds):</label><br>
        <input type="number" name="draw_interval" required><br><br>
        
        <button type="submit">Start Raffle</button>
    </form>
    """

# Timer function to draw ticket numbers
def start_draws():
    def draw():
        global current_draw_index, ticket_numbers
        remaining_tickets = [num for num in ticket_numbers if num not in drawn_numbers]
        
        if len(remaining_tickets) > 1:  # Continue drawing if more than one ticket remains
            # Randomly select a ticket from remaining tickets
            drawn_ticket = random.choice(remaining_tickets)
            drawn_numbers.append(drawn_ticket)
            current_draw_index = ticket_numbers.index(drawn_ticket)
            Timer(draw_interval, draw).start()
        elif len(remaining_tickets) == 1:
            # Last remaining ticket is the winner
            raffle_details["winner"] = remaining_tickets[0]
            drawn_numbers.append(raffle_details["winner"])
            log_winner_to_file()

    draw()

def log_winner_to_file():
    """Logs the raffle results to a text file once the winner is determined."""
    if raffle_details["winner"] is not None:
        with open("raffle_results.txt", "a") as f:
            # Record the current date and time
            now = datetime.now()
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            
            # Write details to the file
            f.write(f"Date: {timestamp}, Winning Ticket: {raffle_details['winner']}, Winning Amount: ${raffle_details['winning_amount']}\n")

# Raffle page to display current draw status
@app.route("/raffle")
def raffle_page():
    return render_template_string(
        raffle_template,
        raffle_details=raffle_details,
        ticket_numbers=ticket_numbers,
        current_draw_index=current_draw_index,
        drawn_numbers=drawn_numbers,
        len=len  # Pass the built-in len function to the template
    )

# Run Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Listen on all available network interfaces, port 5000

