import matplotlib
matplotlib.use("Agg")  # Fix: Use non-interactive backend

from flask import Flask, render_template
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import pandas as pd

app = Flask(__name__)

df = pd.read_csv('Netflix Engagement Dataset.csv')

# Function to Generate Histogram Plot
def plot_histogram():
    sns.set_style("whitegrid")
    plt.figure(figsize=(8,5))
    sns.histplot(df["Daily Watch Time (Hours)"], bins=30, kde=True, color="skyblue")
    plt.title("Distribution of Daily Watch Time")
    plt.xlabel("Daily Watch Time (Hours)")
    plt.ylabel("Frequency")
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()
    plt.close()
    return encoded

# Function to Generate Boxplot
def plot_boxplot():
    plt.figure(figsize=(8,5))
    sns.boxplot(x="Subscription Plan", y="Engagement Rate (1-10)", data=df, palette="pastel")
    plt.title("Engagement Rate by Subscription Plan")
    plt.xlabel("Subscription Plan")
    plt.ylabel("Engagement Rate (1-10)")
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()
    plt.close()
    return encoded

def plot_churn_rate():
    plt.figure(figsize=(8,5))
    churn_counts = df.groupby(["Subscription Plan", "Churn Status (Yes/No)"]).size().unstack()
    churn_counts.plot(kind="bar", stacked=True, colormap="coolwarm", figsize=(8, 5))
    plt.title("Churn Rate by Subscription Plan")
    plt.xlabel("Subscription Plan")
    plt.ylabel("Number of Users")
    plt.legend(title="Churn Status", labels=["No", "Yes"])
    
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
    buf.close()
    plt.close()
    return encoded

@app.route("/")
def index():
    hist_url = plot_histogram()
    boxplot_url = plot_boxplot()
    churn_url = plot_churn_rate()
    return render_template("index.html", hist_url=hist_url, boxplot_url=boxplot_url,churn_url=churn_url)

if __name__ == "__main__":
    app.run(debug=True)
