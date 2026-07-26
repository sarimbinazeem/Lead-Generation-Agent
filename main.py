"""
Purpose -> starts the file and co-ordinates everything
"""
import traceback

from parser import parse_prompt
from scraper import search_business


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

        print("\nBusinesses Found:")

        for index,business in enumerate(businesses,start=1):
            print(f"{index}. {business}")
         
    
    except Exception as e:
        print("\nAn error occurred:")
        traceback.print_exc()    


if __name__ == "__main__":
    main()