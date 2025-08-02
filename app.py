from flask import Flask, render_template, request

app = Flask(__name__)

# Movies and available tickets stored here (in-memory)
movies = {
    "HHVM": 10,
    "Kingdom": 8,
    "Devara": 5,
    "Kalki": 7,
    "Joker": 6
}

@app.route('/', methods=['GET', 'POST'])
def home():
    error = None
    if request.method == 'POST':
        name = request.form.get('name')
        movie = request.form.get('movie')
        tickets = request.form.get('tickets')

        # Basic validation
        if not name or not movie or not tickets:
            error = "Please fill in all fields."
            return render_template('index.html', movies=movies, error=error)

        try:
            tickets = int(tickets)
            if tickets <= 0:
                error = "Please enter a positive number of tickets."
                return render_template('index.html', movies=movies, error=error)
        except ValueError:
            error = "Tickets must be a valid number."
            return render_template('index.html', movies=movies, error=error)

        available = movies.get(movie, 0)
        if tickets > available:
            error = f"Sorry, only {available} tickets available for {movie}."
            return render_template('index.html', movies=movies, error=error)

        # Reduce tickets
        movies[movie] -= tickets

        # Show confirmation
        return render_template('confirmation.html', name=name, movie=movie, tickets=tickets)

    # GET request: render home page
    return render_template('index.html', movies=movies, error=error)

if __name__ == "__main__":
    app.run(debug=True)
