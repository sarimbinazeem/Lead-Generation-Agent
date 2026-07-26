"""
Purpose -> handle browser automation and data collection

We use PlayWright for browser automation that can open google
It can do the following:
Open Chrome -> Click Buttons -> Type text -> page loads -> scroll -> read webpage data

After Searching the businness and location through PlayWright, We will extract all the BUSINESS NAME frm the list

"""

from playwright.sync_api import sync_playwright

#we do synchronously

def open_google_maps(page):
    """
    Opens Google Maps

    """

    print("\nOpening Google Maps...")

    page.goto(
        "https://www.google.com/maps",
        timeout=60000
    )

    #Wait for the  browser to render

    page.wait_for_timeout(5000)

    print("Google Maps Loaded.\n")


def perform_search(page, search_query):
    """
    Searches the user query.
    """

    print("Searching...")

    # Locate the search box
    search_box = page.get_by_role( "combobox", name="Search Google Maps"  )

    # Wait until it becomes visible
    search_box.wait_for(state="visible")

    search_box.click()


    #fills search with query
    search_box.fill(search_query)

    page.keyboard.press("Enter")

    print("Waiting for results...")
    #takes time so we do timeout
    page.wait_for_timeout(6000)


    print(f"\nSearch completed for: {search_query}")
    
def search_business(business,location):

    search_query = f"{business} in {location}"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        open_google_maps(page)

        perform_search(page,search_query)

        input("\nPress ENTER to close browser...")

        browser.close()
    