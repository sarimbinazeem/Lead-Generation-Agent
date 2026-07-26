"""
Purpose -> starts the file and co-ordinates everything
"""
import traceback

from parser import parse_prompt
from scraper import search_business

from excel import save_to_excel


def main():
    print("=" * 50)
    print("Lead Generation Agent Started")
    print("=" * 50)

    prompt = input("Enter Your Search Query: ")
    try:
        business_type, location = parse_prompt(prompt)

        print("\nExtraction Successful!")
        print(f"Business Type : {business_type}")
        print(f"Location      : {location}")

        print("\nLaunching browser...")

        businesses = search_business(business_type, location  )  
        filename = save_to_excel(businesses,business_type)


        print("\n" + "=" * 50)
        print("Lead Generation Summary")
        print("=" * 50)

        print(f"Search Query    : {prompt}")
        print(f"Business Type   : {business_type}")
        print(f"Location        : {location}")
        print(f"Leads Collected : {len(businesses)}")
        print(f"Excel File      : {filename}")

        print("\nCollected Leads:")

        for lead in businesses:
            print(lead)
                
    
    except Exception as e:
        print("\nAn error occurred:")
        traceback.print_exc()    


if __name__ == "__main__":
    main()