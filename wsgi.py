"""Application entry point."""
from ll_dash import init_app


app = init_app()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)