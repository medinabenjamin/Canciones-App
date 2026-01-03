import requests


def get_song_list(owner, repo, path=""):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "acordes-app",
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    items = response.json()
    return [
        item["name"]
        for item in items
        if item["name"].endswith((".cho", ".txt", ".chordpro"))
    ]


def get_song_content(owner, repo, filename, path=""):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}/{filename}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "acordes-app",
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    item = response.json()
    download_url = item["download_url"]
    raw = requests.get(download_url, timeout=10)
    raw.raise_for_status()
    return raw.text
