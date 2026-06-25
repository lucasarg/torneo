from app import create_app

# Entry point for local development
app = create_app()

if __name__ == "__main__":
    # Remember: use a proper WSGI server in production (gunicorn, etc.)
    app.run(debug=True)
