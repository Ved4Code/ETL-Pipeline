# ETL_Pipeline for Maharashtra Real State Properties
## Objectives
Scrape the following Mumbai Government website for Real Estate data using Selenium - (https://pay2igr.igrmaharashtra.gov.in/eDisplay/propertydetails)
### Following inputs are used on website:- 
○ District: Mumbai Sub-urbs

○ Taluka: Andheri

○ Village: Bandra

○ Select Year: 2023

○ Enter Doc/Property/CTS/Survey no/Reg. Year: 2023

First 50 entries of the table are scraped that comes after search results are loaded.
API Endpoint is set up from where we can fetch the data based on Document
No. or Year of Registration (not date, but year).
#### Bonus
- Endpoint enabling Partial text search on the buyer's or seller's name
- Endpoint enabling search for the partial address from the other Information column

### API Endpoints
- Scraped Data: (http://localhost:5000/data)
- Based on Document no: (http://localhost:5000/docnosearch?docno=4286)
- Based on Year of Registration (http://localhost:5000/Yearsearch?year=2023)
- Based on partial name search (http://localhost:5000/namesearch?query=Ashok)
- Based on address (http://localhost:5000/addresssearch?address=khar)

***
Copyright © 2023, [Vedant Sultania](https://github.com/Ved4Code)
