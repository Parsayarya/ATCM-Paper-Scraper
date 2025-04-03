import pandas as pd
import os
import requests
from tqdm import tqdm
import time
import urllib.parse
from pathlib import Path

def download_papers(input_file, output_folder="papers"):
    """
    Read the CSV file with accessible links and download the papers
    to a specified folder.
    
    Parameters:
    input_file (str): Path to the CSV file containing paper links
    output_folder (str): Folder to save downloaded papers
    """
    # Read the filtered data with accessible links
    df = pd.read_csv(input_file)
    
    # Check if the dataframe contains the expected columns
    if 'Download_Link' not in df.columns or 'Title' not in df.columns:
        print("Error: CSV file must contain 'Download_Link' and 'Title' columns.")
        return
    
    # Filter rows where Exists is 'Yes' (if that column is present)
    if 'Exists' in df.columns:
        df = df[df['Exists'] == 'Yes']
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")
    
    # Counter for successful and failed downloads
    successful = 0
    failed = 0
    
    # Download each paper with a progress bar
    print(f"Downloading {len(df)} papers to {output_folder}...")
    for i, row in tqdm(df.iterrows(), total=len(df)):
        if pd.notna(row['Download_Link']):
            url = row['Download_Link']
            try:
                # Get file extension from URL or default to .pdf
                parsed_url = urllib.parse.urlparse(url)
                file_extension = os.path.splitext(parsed_url.path)[1]
                if not file_extension:
                    file_extension = '.pdf'
                
                # Create a sanitized filename from the title
                title = row['Title']
                safe_filename = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
                safe_filename = safe_filename.replace(' ', '_')[:100]  # Limit filename length
                
                # Add year if available
                if 'Year' in df.columns and pd.notna(row['Year']):
                    safe_filename = f"{row['Year']}_{safe_filename}"
                
                # Full path for the file
                file_path = os.path.join(output_folder, f"{safe_filename}{file_extension}")
                
                # Download the file
                response = requests.get(url, timeout=30)
                if response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    successful += 1
                    # Print successful download
                    print(f"Downloaded: {os.path.basename(file_path)}")
                else:
                    print(f"Failed to download {title}: HTTP status code {response.status_code}")
                    failed += 1
                
                # Add a small delay to avoid overwhelming the server
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error downloading {title}: {str(e)}")
                failed += 1
    
    # Print summary
    print("\nDownload Summary:")
    print(f"Total papers attempted: {len(df)}")
    print(f"Successfully downloaded: {successful}")
    print(f"Failed to download: {failed}")
    
    # Create a log file with download results
    log_path = os.path.join(output_folder, "download_log.txt")
    with open(log_path, "w") as log_file:
        log_file.write(f"Download Summary:\n")
        log_file.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log_file.write(f"Source file: {input_file}\n")
        log_file.write(f"Total papers attempted: {len(df)}\n")
        log_file.write(f"Successfully downloaded: {successful}\n")
        log_file.write(f"Failed to download: {failed}\n")
    
    print(f"Download log saved to: {log_path}")
    
    return successful, failed

