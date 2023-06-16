import uuid
from pathlib import Path
from openpecha.github_utils import github_publish
import os 
import csv
from datetime import datetime
from github import RateLimitExceededException
import time

token = os.getenv("GITHUB_TOKEN")
home_path = "data"

def get_four_digit_uuid():
    # Generate a UUID4 (random) and convert it to uppercase
    uuid_str = str(uuid.uuid4()).upper()
    
    # Extract the first four characters from the UUID
    four_digit_uuid = uuid_str[:4]
    
    return four_digit_uuid


def get_pairs(main_dir):
    files = list(Path(main_dir).iterdir())
    return files 


def log(id, csv_file):
    with open(csv_file, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([id])


def create_tm_repo(file):
    bo_text = Path(file / "bo.txt").read_text(encoding="utf-8")
    en_text = Path(file / "en.txt").read_text(encoding="utf-8")
    uuid = get_four_digit_uuid()
    repo_path = f"{home_path}/TM{uuid}_LH"
    Path(repo_path).mkdir()
    Path(f"{repo_path}/bo.txt").write_text(bo_text)
    Path(f"{repo_path}/en.txt").write_text(en_text)
    try:
        github_publish(
            path=repo_path,
            org="MonlamAI",
            not_includes=[],
            token = token
        )
    except RateLimitExceededException as e:
        # Get the time at which the rate limit will reset
        reset_time = datetime.fromtimestamp(int(e.raw_headers.get("X-RateLimit-Reset")))

        # Calculate the time to wait before retrying the API call
        wait_time = reset_time - datetime.now()

        # Wait until the rate limit resets
        print(f"Rate limit exceeded. Waiting {wait_time} before retrying...")
        time.sleep(wait_time.total_seconds())
    log(f"TM{uuid}_LH","tm.csv")


def create_tp_repo(file):
    bo_text = Path(file / "bo.txt").read_text(encoding="utf-8")
    en_text = Path(file / "en.txt").read_text(encoding="utf-8")
    uuid = get_four_digit_uuid()
    bo_repo_path = f"{home_path}/BO{uuid}_LH"
    en_repo_path = f"{home_path}/EN{uuid}_LH"
    Path(bo_repo_path).mkdir()
    Path(en_repo_path).mkdir()
    Path(f"{bo_repo_path}/bo.txt").write_text(bo_text)
    Path(f"{en_repo_path}/en.txt").write_text(en_text)
    github_publish(path=bo_repo_path,org="MonlamAI",not_includes=[],token=token)
    github_publish(path=en_repo_path,org="MonlamAI",not_includes=[],token=token)
    log(f"BO{uuid}_LH","tp.csv")
    log(f"EN{uuid}_LH","tp.csv")



def main(home_dir):
    files  = get_pairs(home_dir)
    for file in files:
        create_tm_repo(file)
        break

if __name__ == "__main__":
    path = "TM_lotsawa_house"
    main(path)