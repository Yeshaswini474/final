# app.py

import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import datetime
import re

def extract_title_from_url(url):
    match = re.search(r'/wiki/(.+)', url)
    if match:
        return match.group(1).replace('_', ' ')
    else:
        raise ValueError("Invalid Wikipedia URL")

def get_pageviews(article_title, start, end):
    title_api = article_title.replace(" ", "_")
    url = f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/all-agents/{title_api}/daily/{start}/{end}"
    response = requests.get(url)
    data = response.json()

    if 'items' not in data:
        print(f"No data for {article_title}")
        return pd.DataFrame()

    views = [{
        'date': item['timestamp'][:8],
        'views': item['views']
    } for item in data['items']]

    df = pd.DataFrame(views)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df.rename(columns={'views': article_title}, inplace=True)
    return df

def run_app():
    wiki_url1 = input("Enter Wikipedia URL 1: ")
    wiki_url2 = input("Enter Wikipedia URL 2: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    title1 = extract_title_from_url(wiki_url1)
    title2 = extract_title_from_url(wiki_url2)

    start_fmt = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y%m%d')
    end_fmt = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y%m%d')

    df1 = get_pageviews(title1, start_fmt, end_fmt)
    df2 = get_pageviews(title2, start_fmt, end_fmt)

    merged_df = pd.merge(df1, df2, left_index=True, right_index=True, how='outer').fillna(0)
    print("\nPageview Data:")
    print(merged_df.head())

    plt.figure(figsize=(12, 6))
    plt.plot(merged_df.index, merged_df[title1], label=title1)
    plt.plot(merged_df.index, merged_df[title2], label=title2)
    plt.xlabel("Date")
    plt.ylabel("Pageviews")
    plt.title("Wikipedia Pageviews Comparison")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_app()
