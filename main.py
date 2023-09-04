from github_api import (
    extract_username_from_url,
    fetch_repositories,
    fetch_files_in_repository,
    fetch_file_content,
    evaluate_code_with_gpt3,
)
import time
import os
from dotenv import load_dotenv

load_dotenv()  # Load the .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Common programming file extensions
VALID_EXTENSIONS = [
    ".py",
    ".js",
    ".cpp",
    ".c",
    ".java",
    ".go",
    ".php",
    ".rb",
    ".rs",
    ".swift",
]


def main():
    # Fetch the GitHub user URL from the user
    github_url = input("Enter a GitHub user URL: ")
    username = extract_username_from_url(github_url)

    # Fetch the repositories of the user
    repositories = fetch_repositories(username)
    print(f"Repositories: {repositories}")

    if not repositories:
        print("No repositories found for the given GitHub user.")
        return

    repo_scores = {}  # To store average complexity scores for each repo

    # Loop through all repositories
    for repo_name in repositories:
        files = fetch_files_in_repository(username, repo_name)

        valid_files = [
            f for f in files if any(f.endswith(ext) for ext in VALID_EXTENSIONS)
        ]

        if not valid_files:
            continue  # Skip repos without valid code files

        total_score = 0  # Total complexity score for this repository
        num_files_evaluated = 0  # Number of files evaluated for complexity

        # Loop through valid code files in the repository and evaluate their complexity
        for code_file in valid_files:
            file_content = fetch_file_content(username, repo_name, code_file)
            complexity_score = evaluate_code_with_gpt3(file_content, OPENAI_API_KEY)
            total_score += complexity_score
            num_files_evaluated += 1
            time.sleep(20)  # Introduce a delay between each API call

        # Store the average complexity score for this repository
        repo_scores[repo_name] = total_score / num_files_evaluated

    if not repo_scores:
        print("No valid files were found in the repositories of the given GitHub user.")
        return

    # Identify the repository with the highest average complexity score
    most_complex_repo = max(repo_scores, key=repo_scores.get)
    print(
        f"\nThe most complex repository is: {most_complex_repo} with a score of {repo_scores[most_complex_repo]}"
    )


if __name__ == "__main__":
    main()