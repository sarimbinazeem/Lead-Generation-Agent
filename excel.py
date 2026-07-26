"""
Purpose -> saves it into an excel file

"""

from openpyxl import Workbook

def save_to_excel(leads,business_type):
    """
    Saves all colelcted leads into an excel file
    """

    workbook = Workbook()

    #focus on sheet
    sheet = workbook.active

    sheet.title = "Leads"

    #Header row
    sheet.append([
        "Business Name",
        "Email",
        "Phone Number",
        "Website",
        "Location"
    ])

    # Lead Rows
    for lead in leads:

        sheet.append([
            lead.get("Business Name", ""),
            lead.get("Email", ""),
            lead.get("Phone Number", ""),
            lead.get("Website", ""),
            lead.get("Location", "")
        ])


    #save the file in file_name format
    filename = f"leads_{business_type.replace(' ', '_').lower()}.xlsx"

    workbook.save(filename)   