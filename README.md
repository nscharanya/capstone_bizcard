# capstone_bizcard
This Streamlit app utilizes EasyOCR for Optical Character Recognition (OCR) to extract information from business card images. Users can upload images, extract data like name, contact details, and company information, preview, modify, and delete data, and save it to a PostgreSQL database for efficient management.

#### Required Libraries:
      1) Streamlit
      2) EasyOCR
      3) PIL (Python Imaging Library)
      4) Pandas
      5) NumPy
      6) re (regular expressions)
      7) io
      8) psycopg2 (PostgreSQL adapter)
      9) os
      
#### Step-by-Step Process to create the Project:

      1) image_to_text_conversion : A function image_to_text_conversion is defined that takes the path of an image, reads the image, converts it to an array, and then uses 
                                    EasyOCR to perform Optical Character Recognition (OCR) to extract text data from the image.

      2) extracted_text : A function extracted_text is defined that takes the extracted text from the image and processes it to extract specific fields such as name, 
                          designation, company name, contact information, email, website, address, and pincode.
                          
      3) Streamlit UI : A Streamlit user interface (UI) is created with a wide layout and the main menu is defined using st.sidebar.title and st.sidebar.radio for navigation 
                        between sections (Home, Upload & Modifying, Delete)
                        
      4) Home Section : In the Home section, an overview of the project, its key features, technologies used, and the developer's information is provided.
      
      5) Upload & Modifying Section : This section allows users to upload business card images, extract text data, display the extracted data along with the uploaded image, 
                                      save the data to a PostgreSQL database and it also allows users to preview and modify the data.
                                      
                                      (i) : Preview Data: Users can preview the data extracted from business cards stored in the PostgreSQL database.
                                      
                                      (ii) : Modify Data: Users can select a name, modify the details such as name, designation, company name, contact, email, website, 
                                                          address, pincode, and image URL, and save the modified data back to the database.
                                                          
      6) Delete Data: Users can select a name and designation to delete specific entries from the PostgreSQL database.

In conclusion, the Business Card Data Extraction with OCR project offers a solution for individuals to quickly and accurately gather important details from business cards.  Users can easily preview, modify, and delete extracted data, facilitating seamless data management. With the ability to save data to a PostgreSQL database, this project not only saves time and effort but also enhances data organization and accessibility.
                                      
