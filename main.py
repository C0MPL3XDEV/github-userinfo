import requests
import argparse
import json
import os

parser = argparse.ArgumentParser(description="Github User-Info")
parser.add_argument("--username", type=str, required=True, help="GitHub username to fetch events")

args = parser.parse_args()
username = args.username

def json_parser(file):
    with open(file, 'r') as json_file:
        all_data = json.load(json_file)

    for event in all_data:  # Ciclo per ogni evento
        print(f"Event Type: {event['type']}")
        print(f"Actor: {event['actor']['login']}")
        print(f"Repository: {event['repo']['name']}")
        print(f"Action: {event['payload'].get('action', 'N/A')}")
        print(f"Created At: {event['created_at']}")
        print("Commits:")

        if event['type'] == "PushEvent":
            for commit in event['payload'].get('commits', []):
                print(f"  - SHA: {commit['sha']}")
                print(f"    Author: {commit['author']['name']}")
                print(f"    Message: {commit['message']}")
                print(f"    URL: {commit['url']}")

        print("\n")

def request_data(username):
    URL = f"https://api.github.com/users/{username}/events"
    headers = {'X-GitHub-Api-Version': '2022-11-28'}
    
    try:
        response = requests.get(url=URL, headers=headers)
        response.raise_for_status()  # Solleva un'eccezione per codici di errore HTTP

        fetched_data = response.json()

        try:
            with open("response.json", "r") as r:
                existing_data = json.load(r)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            existing_data = []

        existing_data.extend(fetched_data)  # Aggiunge i nuovi dati a quelli esistenti

        with open('response.json', "w") as r:
            json.dump(existing_data, r, indent=4)

        json_parser(file="response.json")     

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")

request_data(username=username)

os.remove("response.json")   
