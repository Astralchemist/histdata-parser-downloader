# main.py

from config import PAIRS, YEAR
from downloader import download_with_selenium, get_histdata_filename
from extractor import extract_zip
import os
from datetime import datetime

def run():
    # Ensure the 'data' and 'downloads' directories exist
    os.makedirs("data", exist_ok=True)
    os.makedirs("downloads", exist_ok=True)

    # Track failed downloads
    failed_downloads = []
    max_retries = 3

    for pair in PAIRS:
        for month in range(1, 13):
            retry_count = 0
            success = False

            while not success and retry_count < max_retries:
                if retry_count > 0:
                    print(f"Retry attempt {retry_count} for {pair} {YEAR}-{month:02d}")

                print(f"Processing {pair} {YEAR}-{month:02d}")

                # Use HistData's file naming convention
                zip_name = get_histdata_filename(pair, YEAR, month)
                zip_path = os.path.join("downloads", zip_name)
                extract_to = os.path.join("data", pair)

                # Ensure the pair-specific directory exists for extraction
                os.makedirs(extract_to, exist_ok=True)

                # Download data using Selenium
                download_with_selenium(pair, YEAR, month)

                # Check all possible variations of the filename
                base_name = zip_name[:-4]  # Remove .zip extension
                possible_files = [
                    zip_path,
                    os.path.join("downloads", f"{base_name} (1).zip"),
                    os.path.join("downloads", f"{base_name} (2).zip"),
                    os.path.join("downloads", f"{base_name} (3).zip")
                ]

                # Try to find and extract any matching file
                file_found = False
                for possible_file in possible_files:
                    if os.path.exists(possible_file):
                        try:
                            extract_zip(possible_file, extract_to)
                            success = True
                            file_found = True
                            break
                        except Exception as e:
                            print(f"Error extracting {os.path.basename(possible_file)}: {str(e)}")
                
                if not file_found:
                    print(f"❌ No matching ZIP file found for {zip_name}")
                    retry_count += 1

            if not success:
                failed_downloads.append((pair, YEAR, month))
                print(f"⚠️ Failed to process {pair} for {YEAR}-{month:02d} after {max_retries} attempts")

    # Print summary at the end
    print("\n=== Download Summary ===")
    print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    if failed_downloads:
        print("\nFailed Downloads:")
        for pair, year, month in failed_downloads:
            print(f"- {pair} {year}-{month:02d}")
        
        # Save failed downloads to a file for later retry
        with open("failed_downloads.txt", "w") as f:
            for pair, year, month in failed_downloads:
                f.write(f"{pair},{year},{month}\n")
        print("\nFailed downloads have been saved to 'failed_downloads.txt'")
    else:
        print("\nAll downloads completed successfully! 🎉")

if __name__ == "__main__":
    run()
