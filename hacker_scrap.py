import csv
import requests
import browser_cookie3

def get_cookies():
    try:
        cookies = browser_cookie3.chrome(domain_name='hackerrank.com')
    except:
        cookies = browser_cookie3.firefox(domain_name='hackerrank.com')

    return cookies


def fetch_leaderboard(slug, limit=500):
    url = f"https://www.hackerrank.com/rest/contests/{slug}/leaderboard"

    params = {
        "offset": 0,
        "limit": limit
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    cookies = get_cookies()

    response = requests.get(url, params=params, headers=headers, cookies=cookies)

    if response.status_code != 200:
        print("Failed:", response.status_code)
        print(response.text[:300])
        return None

    return response.json().get("models", [])


def save_to_csv(slug, data):
    filename = f"leaderboard-{slug}.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Rank", "Username", "Score", "Time_Taken"])

        for entry in data:
            writer.writerow([
                entry.get("rank"),
                entry.get("hacker"),
                entry.get("score"),
                entry.get("time_taken")
            ])

    print("Saved:", filename)


def main():
    slug = input("Enter private contest slug (example: my-campus-contest): ")

    print("Fetching leaderboard...")
    data = fetch_leaderboard(slug)

    if not data:
        print("No leaderboard data found. Are you logged in on browser?")
        return

    save_to_csv(slug, data)


if __name__ == "__main__":
    main()
