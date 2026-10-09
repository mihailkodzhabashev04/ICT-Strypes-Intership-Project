from pathlib import Path
from datetime import datetime

from scrapers.books import scrape_books
from scrapers.quotes import scrape_quotes
from storage import save_json

OUTPUT_DIR = Path('output')

WEBSITES = {
    "1":{"name": "Books to Scrape",
         "scraper": scrape_books,
         "data_types": [
             "Book Title",
             "Price",
             "Availability",
             "Rating",
             "Category"
         ]},
    "2":{"name": "Quotes to Scrape",
         "scraper": scrape_quotes,
         "data_types": [
             "Quote Text",
             "Author",
             "Tags"
         ],},


}

EXIT_KEY = str(len(WEBSITES) + 1)

def display_menu():
    """
    Displaying the menu screen
    """
    print("Available websites to scrape:")

    for i, website in WEBSITES.items():
        print(f"{i}. {website['name']}")

    print(f"{EXIT_KEY}. Exit")


def run_scraper(site, session_summary):
    """
    Run the scraper, save the results to a JSON file
    and display the completion summary.
    """

    print(f"\nScraping...   {site['name']}")

    #Run the scraper for the give website
    try:
        records = site['scraper']()

    except Exception as e:
        print(f"Error: {e}")

    #In case nothing was scraped.
    if not records:
        print(f"No records found for {site['name']}")
        return

    #Creating a unique filename to avoid overwriting files
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    save_name = site['name'].lower().replace(" ", "_")
    output_path = OUTPUT_DIR / f"{save_name}_{timestamp}.json"

    #Save the scraped data
    try:
        saved_path = save_json(records, output_path)
    except OSError as e:
        print(f"The data was scraped, but could not be saved.\nDetails: {e}")

    #Displaying the summary
    print("\nScraping successful!")
    print(f"Website: {site['name']}")

    print("Scraped data:")

    for data_type in site['data_types']:
        print(f"{data_type}")

    print(f"Records collected: {len(records)}")
    print(f"Data saved to {saved_path}")

    #Store information about this operation.
    session_summary.append(
        {
            "website": site['name'],
            "output": str(saved_path),
            "data_types": site['data_types'],
            "records": len(records),
        }
    )


def display_session_summary(session_summary):
    """
    Displaying the session summary screen.
    """

    print(f"\nSession summary:")

    if not session_summary:
        print(f"No successful scraping operation completed.")
        return

    for index, record in enumerate(session_summary, start=1):
        print(f"\n{index}. {record['website']}")
        print(f"   Records collected: {record['records']}")
        print(f"   Data types: {', '.join(record['data_types'])}")
        print(f"   Output: {record['output']}")



session_summary = []

print("Welcome to the Web Scraper."
      "chose a website to scrape.")


while True:
    display_menu()

    choice = input("\n Select an option: ").strip()

    if choice == EXIT_KEY:
        display_session_summary(session_summary)

        print("Thank you for using the scraper.")
        break


    if choice not in WEBSITES:
        print(f"Invalid choice. Please try again. Choices available are from 1 to {EXIT_KEY}")
        continue

    run_scraper(WEBSITES[choice], session_summary)

