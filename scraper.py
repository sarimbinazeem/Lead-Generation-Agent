"""
Purpose -> handle browser automation and data collection

We use PlayWright for browser automation that can open google
It can do the following:
Open Chrome -> Click Buttons -> Type text -> page loads -> scroll -> read webpage data

After Searching the businness and location through PlayWright, We will extract all the Business (as Buttons) from the list

We click on the business button one by one and extracts its information from its details section

"""

import re

from playwright.sync_api import sync_playwright

#we do synchronously

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

        #context will have multiple pages instead of having only one at a tme
        context = browser.new_context()

        page = context.new_page()


        open_bing_maps(page)

        perform_bing_search(page, search_query)


        business_indexes = collect_business_indexes(page)

        leads = []

        for index in business_indexes:

            buttons = page.get_by_role("button")

            button = buttons.nth(index)

            lead = extract_business_details(page, button)

            if lead is not None:
                lead["Location"] = location
                #we append if there exists entries
                if (
                        lead["Business Name"] != ""
                        or lead["Phone Number"] != ""
                        or lead["Website"] != ""
                ):
                 leads.append(lead)



        input("\nPress ENTER to close browser...")
        context.close()
        browser.close()

        return leads

def collect_business_indexes(page):
    """
    Collects the indexes of business buttons.
    """

    print("\nCollecting business buttons...")

    #the buttons are the business in BING Layout so we store it here
    buttons = page.get_by_role("button")

    business_indexes  = []

    #we loop through the buttons and put VALID Business name into the array
    count = buttons.count()

    for i in range(count):

        try:

            text = buttons.nth(i).inner_text().strip()
            #Skip if it is EMPTY button
            if not text:
                continue

            lines = text.split("\n")
            #Skip if the button name is LONGER Than 3 LINES!
            if len(lines) < 3:
                continue

            # Skip utility buttons
            if lines[0] in ["Rating", "Hours", "Feedback"]:
                continue

            business_indexes.append(i)

        except Exception:
            continue

    print(f"Business buttons collected: {len(business_indexes)}")

    return business_indexes


def extract_business_details(page,button):
    """
    Click business button
    extract all information from details page
    """

    try:
        button.click()
        page.wait_for_timeout(3000)

        links = page.get_by_role("link")

        lead={
            "Business Name": "",
            "Phone Number": "",
            "Website": "",
            "Location": "",
            "Email": ""
        }

        #lOOP THROUGH LINKS and store into lead for relevant info
        count = links.count()

        for i in range(count):
            try:
                text = links.nth(i).inner_text().strip()

                if not text:
                    continue

                #Website

                if text.startswith("http"):

                    lead["Website"] = text.replace("›", "").strip()

                    continue                

                #Phone Number
                if text.startswith("+"):

                    lead["Phone Number"] = text

                    continue

                if (
                    len(text) > 3
                    and "http" not in text.lower()
                    and "+" not in text
                    and "Directions" not in text
                    and "Sign in" not in text
                    and "reviews" not in text.lower()
                    and "all images" not in text.lower()
                    and "openstreetmap" not in text.lower()
                    and "tripadvisor" not in text.lower()
                    and "view full review" not in text.lower()
                    and "see all reviews" not in text.lower()
                ):

                    if lead["Business Name"] == "":
                        lead["Business Name"] = text
                        

            except:
                continue


    except Exception:
        print("Couldn't click business.")
        return None

    lead["Email"] = find_email(
        page,
        lead["Website"]
    )
    return lead

def find_email(page,website):
    """
    Visit the business website

    Finds email from the website
    """


    if website == "":
        return ""

    website_page = page.context.new_page()
    try:
        website_page.goto(
            website,
            timeout=15000
        )

        website_page.wait_for_timeout(3000)

        text = website_page.locator("body").inner_text()

        #find email in the text 
        emails = re.findall(

            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

            #[user] + @[email].[TDL] 

            text
        )

        if emails:
            return emails[0]

    except Exception:
        pass

    finally:
        website_page.close()

    return ""