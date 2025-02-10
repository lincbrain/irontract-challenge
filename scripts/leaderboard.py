import os
import re

RESULTS_DIR = "results"
README_FILE = "README.md"

def parse_score_from_file(filepath):
    """
    Opens the file at `filepath`, reads its lines, and extracts the AUC score
    from the last line assuming it follows the format:
    "Area Under Curve (AUC): 0.2222"
    """
    with open(filepath, "r") as file:
        lines = file.readlines()
        if not lines:
            return None
        last_line = lines[-1].strip()
        # Use regex to extract the numeric score from the expected format.
        match = re.search(r"Area Under Curve \(AUC\):\s*([\d\.]+)", last_line)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
        return None

def get_all_scores():
    """
    Walks through the RESULTS_DIR and returns a list of dictionaries,
    each containing the 'username' (derived from the filename) and the extracted 'score'.
    """
    scores = []
    for filename in os.listdir(RESULTS_DIR):
        if filename.endswith(".txt"):
            username = filename[:-4]  # Remove the ".txt" extension to get the username.
            filepath = os.path.join(RESULTS_DIR, filename)
            score = parse_score_from_file(filepath)
            if score is not None:
                scores.append({"username": username, "score": score})
    return scores

def generate_markdown_table(scores):
    """
    Sorts the scores (higher is better) and generates a Markdown table.
    """
    # Sort by score in descending order.
    scores_sorted = sorted(scores, key=lambda x: x["score"], reverse=True)
    table = "| Rank | Username | AUC Score |\n"
    table += "|------|----------|-----------|\n"
    for rank, entry in enumerate(scores_sorted, start=1):
        table += f"| {rank} | {entry['username']} | {entry['score']:.4f} |\n"
    return table

def update_readme():
    """
    Reads the README_FILE, finds the section delimited by the markers,
    and replaces that section with the newly generated leaderboard table.
    """
    # Get the leaderboard table based on current results.
    scores = get_all_scores()
    leaderboard_table = generate_markdown_table(scores)
    
    # Read the current README.md content.
    with open(README_FILE, "r") as file:
        lines = file.readlines()
    
    # Define the start and end markers.
    start_marker = "<!-- START_LEADERBOARD -->"
    end_marker = "<!-- END_LEADERBOARD -->"
    
    # Find the indices of the markers.
    try:
        start_index = next(i for i, line in enumerate(lines) if start_marker in line)
        end_index = next(i for i, line in enumerate(lines) if end_marker in line)
    except StopIteration:
        print("Markers not found in README.md. Please add them before running the script.")
        return

    # Replace the content between the markers.
    new_content = (
        lines[:start_index + 1] +
        ["\n", leaderboard_table, "\n"] +
        lines[end_index:]
    )

    # Write the updated content back to README.md.
    with open(README_FILE, "w") as file:
        file.writelines(new_content)
    print("README.md updated successfully with the leaderboard.")

if __name__ == "__main__":
    update_readme()