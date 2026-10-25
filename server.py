from flask import Flask

app = Flask(__name__)

@app.route("/health")
def healthCheck():
    return "Flask server is up and running"

@app.route("/analyze-stock/<ticker>")
def  analyzeStock(ticker):
    return {"data": f"Analysis for {ticker} coming soon!"}
if __name__ == "__main__":
    app.run()