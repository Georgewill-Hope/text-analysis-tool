from flask import Flask, abort

app = Flask(__name__)

@app.route("/health")
def healthCheck():
    return "Flask server is up and running"

@app.route("/analyze-stock/<ticker>")
def  analyzeStock(ticker):
    
    if len(ticker) > 5 or not ticker.isidentifier():
        abort(400, "Invalid ticker symbol")
    return {"data": f"Analysis for {ticker} coming soon!"}
if __name__ == "__main__":
    app.run()