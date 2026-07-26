"""
Purpose -> handle browser automation and data collection

We use PlayWright for browser automation that can open google
It can do the following:
Open Chrome -> Click Buttons -> Type text -> page loads -> scroll -> read webpage data

"""

from playwright.sync_api import sync_playwright

#we do synchronously

def search_business(business,location):
    """
    Helper Function
    it launches chrome
    it takes new page
    goes to GOOOGLE map through URL
    Searches the query through search box
    """

    search_query = f"{business} in {location}"

    #opens the playwright synchronusly
    with sync_playwright() as p:
        browser= p.chromium.launch(
            headless=False, #opens the browser visibly
        )

        #takes page
        page = browser.new_page()

        print("\nOpening Google Maps...")
        #Open maps through URL
        page.goto(
             "https://www.google.com/maps",
             timeout=60000 #60 seconds timeout
        )   
        print(f"Page Title: {page.title()}")

        # Give Google Maps time to fully render
        page.wait_for_timeout(5000)

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

        input("\nPress ENTER to close the browser...")

        browser.close()        