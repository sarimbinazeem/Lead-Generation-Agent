"""
Purpose -> starts the file and co-ordinates everything
"""

from parser import parse_prompt


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
    
    except Exception as e:
        print("\nAn error occurred while parsing the prompt.")
        print(e)      


if __name__ == "__main__":
    main()