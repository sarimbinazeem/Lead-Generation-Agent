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

def open_bing_maps(page):
    """
    Opens Bing Maps.
    """

    print("\nOpening Bing Maps...")

    page.goto(
        "https://www.bing.com/maps",
        timeout=60000
    )
    #renders
    page.wait_for_timeout(5000)

    print("Bing Maps Loaded.\n")


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

    page.wait_for_timeout(8000)

    print("\nCurrent URL:")
    print(page.url)

    print("Waiting for results...")
    #takes time so we do timeout
    page.wait_for_timeout(6000)


    print(f"\nSearch completed for: {search_query}")

def perform_bing_search(page, search_query):
    """
    Searches Bing Maps.
    """

    print(f"Searching for: {search_query}")

    search_box = page.get_by_role( "combobox", name="Search Bing Maps")

    search_box.click()

    search_box.press("Control+A")
    search_box.press("Backspace")

    search_box.fill(search_query)


    search_box.press("Enter")

    print("Waiting for search results...")

    page.wait_for_timeout(6000)

    print("Search completed.\n")    
    
def search_business(business,location):

    search_query = f"{business} in {location}"

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False
        )

        page = browser.new_page()

        open_bing_maps(page)

        perform_bing_search(page, search_query)

        input("\nPress ENTER to close browser...")

        businesses = collect_business_names(page)
        browser.close()

        return businesses


def collect_business_names(page):
    """
    Collects the business name from the list of the search results

    """

    print("Collecting business names...\n")

    business_names = []

    #the buttons are the business in BING Layout so we store it here
    buttons = page.get_by_role("button")

    #we loop through the buttons and put VALID Business name into the array
    count = buttons.count()

    print(f"Businesses detected: {count}")

    for i in range(count):
        try:
            name = buttons.nth(i).inner_text().strip()

            #Skip if it is EMPTY button
            if not name:
                continue

            lines = name.split("\n")
            #Skip if the button name is LONGER Than 3 LINES!
            if len(lines) < 3:
                continue  

            # Skip utility buttons
            if lines[0] in ["Rating", "Hours", "Feedback"]:
                continue

            business_name = lines[0].strip()

            if business_name not in business_names:
                business_names.append(business_name)

        except Exception:
            continue

    return business_names
