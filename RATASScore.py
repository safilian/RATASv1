import os
import json
import csv

def extract_score_breakdown(folder_path, output_csv):
    # Prepare the CSV file
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["File Name", "Index", "Score Value"])  # Header row
        
        # Loop through all JSON files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".json"):  # Process only JSON files
                file_path = os.path.join(folder_path, filename)
                
                try:
                    # Read the JSON file
                    with open(file_path, 'r', encoding='utf-8') as file:
                        data = json.load(file)

                        # Check if the root node contains score_breakdown
                        if "score_breakdown" in data:
                            score_breakdown = data["score_breakdown"]

                            # Ensure score_breakdown is a dictionary
                            if isinstance(score_breakdown, dict):
                                # Extract only values where x is even in 1.x
                                for key, value in score_breakdown.items():
                                    if key.startswith("1."):
                                        try:
                                            x = int(key.split(".")[1])
                                            if x % 2 == 0:  # Ensure x is even
                                                csv_writer.writerow([filename, x // 2, value])
                                        except ValueError:
                                            continue  # Skip non-integer x values
                            else:
                                print(f"Warning: 'score_breakdown' is not a dictionary in {filename}")

                except json.JSONDecodeError:
                    print(f"Error: Failed to parse {filename} as valid JSON.")
                except Exception as e:
                    print(f"Error processing {filename}: {e}")


# Usage example
folder_path = "output_ReflectiveJournal_light"  # Change this to the correct folder path
output_csv = "RATASScoreExcelFinal.csv"  # Change this to the desired output file path
extract_score_breakdown(folder_path, output_csv)

print(f"CSV file generated successfully: {output_csv}")
