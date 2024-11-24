import os
import subprocess
import requests

# GitHub Token and Username
GITHUB_USERNAME = "slanwa"
GITHUB_TOKEN = "your_github_token_here"  # Replace with your personal access token

# Function to create a GitHub repository
def create_github_repo(repo_name):
    url = "https://api.github.com/user/repos"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "name": repo_name,
        "private": False,  # Set to True if you want the repository to be private
    }

    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 201:
        print(f"Successfully created repository: {repo_name}")
        return f"https://github.com/{GITHUB_USERNAME}/{repo_name}.git"
    else:
        print(f"Failed to create repository: {response.json()}")
        return None

# Function to push code to GitHub
def push_to_github(repo_url, local_repo_path):
    try:
        os.chdir(local_repo_path)  # Change to the local repository directory

        # Initialize Git
        subprocess.run(["git", "init"], check=True)

        # Add files to staging
        subprocess.run(["git", "add", "."], check=True)

        # Commit files
        subprocess.run(["git", "commit", "-m", "Initial commit"], check=True)

        # Add the remote origin
        subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)

        # Push to GitHub
        subprocess.run(["git", "branch", "-M", "main"], check=True)  # Ensure branch is "main"
        subprocess.run(["git", "push", "-u", "origin", "main"], check=True)

        print("Code pushed to GitHub successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Error during Git operations: {e}")
    except Exception as ex:
        print(f"Unexpected error: {ex}")

# Main script
if __name__ == "__main__":
    repo_name = input("Enter the name of the GitHub repository: ")
    local_repo_path = input("Enter the full path to your local repository: ")

    # Step 1: Create GitHub repository
    repo_url = create_github_repo(repo_name)
    if not repo_url:
        print("Repository creation failed. Exiting.")
        exit(1)

    # Step 2: Push local repository to GitHub
    push_to_github(repo_url, local_repo_path)
