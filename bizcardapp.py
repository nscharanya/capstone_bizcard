import streamlit as st
import easyocr   # Optical Character Recognition
from PIL import Image # for working with images in Python (Python imaging Library)
import pandas as pd
import numpy as np
import re                # For regular expressions
import io                # Input- output
import psycopg2
              

def image_to_text_conversion(path):
  input_img = Image.open(path)

  # Converting image into array format
  img_array = np.array(input_img)

  reader = easyocr.Reader(['en']) # The OCR reader should be set up to recognize text in English
  # The text should be recognised and read from the image array
  text = reader.readtext(img_array, detail = 0)  # detail = 0 returns only the recognized text without any additional details or annotations like arrays
  return text, input_img

def extracted_text(img_text):
    extracted_text_dict = {"NAME" : [],
                        "DESIGNATION" : [],
                        "COMPANY_NAME" : [],
                        "CONTACT" : [],
                        "EMAIL" : [],
                        "WEBSITE" : [],
                        "ADDRESS" : [],
                        "PINCODE" : []}
    extracted_text_dict["NAME"].append(img_text[0])
    extracted_text_dict["DESIGNATION"].append(img_text[1])

    for i in range(2, len(img_text)):
        if img_text[i].startswith("+") or (img_text[i].replace("-", "").isdigit() and '-' in img_text[i]):
            extracted_text_dict["CONTACT"].append(img_text[i])

        elif "@" in img_text[i] and ".com" in img_text[i]:
            extracted_text_dict["EMAIL"].append(img_text[i])
        
        elif "WWW" in img_text[i] or "www" in img_text[i] or "Www" in img_text[i] or "wWw" in img_text[i] or "wwW" in img_text[i]:
            small = img_text[i].lower() # Converting any format of "WWW" into lower case
            extracted_text_dict["WEBSITE"].append(small)  

        elif "Tamil Nadu" in img_text[i] or "TamilNadu" in img_text[i] or img_text[i].isdigit():
            extracted_text_dict["PINCODE"].append(img_text[i])

        elif re.match(r'^[A-Za-z]', img_text[i]): # checks if the pattern(a-zA-Z) matches at the beginning of the string.
            extracted_text_dict["COMPANY_NAME"].append(img_text[i])
        
        else:
            remove_semico_com = re.sub(r'[,;]', '', img_text[i]) # The left over one is address. re.sub() removes , and ; from the address
            extracted_text_dict["ADDRESS"].append(remove_semico_com)
        
    
    for key, value in extracted_text_dict.items():
        if len(value)>0:       
            concatenate = " ".join(value)      
            extracted_text_dict[key] = [concatenate]
        
        else:
            value = "NA"         # Because few addresses have null values
            extracted_text_dict[key] = [value]
    return extracted_text_dict


# Streamlit part
st.set_page_config(layout = 'wide')
st.title("EXTRACTING BUSINESS CARD DATA WITH 'OCR' 📇")

st.sidebar.title("Main Menu \U0001F4DD")
select = st.sidebar.radio("", ["Home", "Upload & Modifying", "Delete"])

if select == "Home":
    st.write("")
    st.write("### \U0001F3E0 You are currently viewing the Home section ")
    st.write("")
    st.write("")
    st.markdown("##### \U0001F4C7  Welcome to Business Card Data Extraction with OCR   📇")
    st.write("This application helps you extract text data from business cards using Optical Character Recognition (OCR).")
    st.write("\U0001F511 Key features:")
    st.write("- Upload an image of a business card (PNG, JPG, JPEG formats supported).")
    st.write("- Extracted data includes name, designation, company name, contact information, email, website, address, and pincode.")
    st.write("- Preview, modify, and delete extracted data.")
    st.write("- Save extracted data to a PostgreSQL database.")
    st.write("Get started by navigating to 'Upload & Modifying' in the sidebar.")

    st.markdown("### 🛠️ How it works:")
    st.write("1. Upload an image of a business card.")
    st.write("2. The app uses OCR to extract text data from the image.")
    st.write("3. Extracted data is displayed, and you can preview, modify, or delete it.")
    st.write("4. Modified data can be saved back to the database.")

    st.markdown("### \U0001F4BB Technologies used:")
    st.write("\U0001F40D - Python Programming language for writing the code")
    st.write("\U0001F680 - Streamlit for the web app interface.")
    st.write("\U0001F4D6 - EasyOCR library for Optical Character Recognition.")
    st.write("\U0001F418 - PostgreSQL for database management.")

    st.markdown("### \U0001F914 Why use this app?")
    st.write("- Save time and effort by automatically extracting business card data.")
    st.write("- Organize and manage business card information in a database.")
    st.write("- Easily preview, modify, and delete data as needed.")

    st.write("")
    st.markdown("##### About the developer:")
    st.write("This app is developed by - NEMMADI SAI CHARANYA.")
    st.write("")
    st.write("")
    st.markdown("<p style='text-align: center;'>THANKS FOR VIEWING \U0001F60A</p>", unsafe_allow_html=True)

    
elif select == "Upload & Modifying":
    st.write("### \U0001F504 You are currently viewing the Upload & Modifying section")
    img = st.file_uploader("Upload the Image", type = ["png", "jpg", "jpeg"])

    if img is not None:
        st.image(img, caption='Uploaded Image', use_column_width=True)

        img_text , input_img = image_to_text_conversion(img)

        text_dict = extracted_text(img_text)

        if text_dict:     # True --> If any value exists in text_dict 
            st.success("TEXT IS EXTRACTED SUCCESSFULLY")

        df = pd.DataFrame(text_dict)

        # Converting image (input_img) to binary format (image_data)
        Image_bytes = io.BytesIO()
        input_img.save(Image_bytes, format='PNG')
        image_data = Image_bytes.getvalue()

        # Creating a dataframe(df1) containing image_data and combining it with df side by side and display them using st.dataframe()
        data = {"IMAGE" : [image_data]}
        df1 = pd.DataFrame(data)
        concat_df = pd.concat([df,df1], axis = 1)
        st.dataframe(concat_df)

        button_1 = st.button("Save", use_container_width=True)

        if button_1:
            mydb = psycopg2.connect(host = "localhost",
                                user = "postgres",
                                password = "Charanya@09",
                                database = "bizcard",
                                port = 5432
                                )
            cursor = mydb.cursor()

            create_table_query = '''CREATE TABLE if not exists bizcard_details(name varchar(255),
                                                                            designation varchar(255),
                                                                            company_name varchar(255),
                                                                            contact varchar(255),
                                                                            email varchar(255),
                                                                            website text,
                                                                            address text,
                                                                            pincode varchar(255),
                                                                            image text)'''

            cursor.execute(create_table_query)
            mydb.commit()

            insert_query = '''INSERT INTO bizcard_details(name, designation, company_name, contact, email, website,
                                                        address, pincode, image)
                                                        
                                                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

            values = (df.loc[0, "NAME"],
                    df.loc[0, "DESIGNATION"],
                    df.loc[0, "COMPANY_NAME"],
                    df.loc[0, "CONTACT"],
                    df.loc[0, "EMAIL"],
                    df.loc[0, "WEBSITE"],
                    df.loc[0, "ADDRESS"],
                    df.loc[0, "PINCODE"],
                    df1.loc[0, "IMAGE"])
            cursor.execute(insert_query, values)
            mydb.commit()

            st.success("SAVED SUCCESSFULLY")

    method = st.selectbox("Select the Method", ["None", "Preview", "Modify"])

    if method == "None":
        st.write("Welcome! This is the default content for the Upload & Modifying section.")   

    elif method == "Preview":

        mydb = psycopg2.connect(host = "localhost",
                                user = "postgres",
                                password = "Charanya@09",
                                database = "bizcard",
                                port = 5432
                                )
        cursor = mydb.cursor()
        select_query = '''SELECT* FROM bizcard_details'''
        cursor.execute(select_query)
        table = cursor.fetchall()
        mydb.commit()

        table_df = pd.DataFrame(table, columns = ("NAME", "DESIGNATION", "COMPANY_NAME", "CONTACT", "EMAIL", "WEBSITE",
                                                "ADDRESS", "PINCODE", "IMAGE"))
        st.dataframe(table_df)

    elif method == "Modify":
        mydb = psycopg2.connect(host="localhost", user="postgres", password="Charanya@09", database="bizcard", port=5432)
        cursor = mydb.cursor()

        select_query = '''SELECT * FROM bizcard_details'''
        cursor.execute(select_query)
        table = cursor.fetchall()
        mydb.commit()

        table_df = pd.DataFrame(table, columns=("NAME", "DESIGNATION", "COMPANY_NAME", "CONTACT", "EMAIL", "WEBSITE",
                                                "ADDRESS", "PINCODE", "IMAGE"))

        selected_name = st.selectbox("Select the name", table_df["NAME"])

        df_3 = table_df[table_df["NAME"] == selected_name]
        df_4 = df_3.copy()

        col1,col2 = st.columns(2)

        with col1:
            modify_name = st.text_input("Name", df_3["NAME"].unique()[0])
            modify_designation = st.text_input("Designation", df_3["DESIGNATION"].unique()[0])
            modify_comp_name = st.text_input("Company_Name", df_3["COMPANY_NAME"].unique()[0])
            modify_contact = st.text_input("Contact", df_3["CONTACT"].unique()[0])
            modify_email = st.text_input("Email", df_3["EMAIL"].unique()[0])

            # Copying the modified details into df_4 which has already copied df_3
            df_4["NAME"] = modify_name
            df_4["DESIGNATION"] = modify_designation
            df_4["COMPANY_NAME"] = modify_comp_name
            df_4["CONTACT"] = modify_contact
            df_4["EMAIL"] = modify_email

        with col2:
            modify_website = st.text_input("Website", df_3["WEBSITE"].unique()[0])
            modify_address = st.text_input("Address", df_3["ADDRESS"].unique()[0])
            modify_pincode = st.text_input("Pincode", df_3["PINCODE"].unique()[0])
            modify_image = st.text_input("Image", df_3["IMAGE"].unique()[0])

            df_4["WEBSITE"] = modify_website
            df_4["ADDRESS"] = modify_address
            df_4["PINCODE"] = modify_pincode
            df_4["IMAGE"] = modify_image

        st.dataframe(df_4)

        button_2 = st.button("Modify", use_container_width=True)

        if button_2:
            cursor.execute(f"DELETE FROM bizcard_details WHERE name = '{selected_name}' ")
            mydb.commit()

            insert_query = '''INSERT INTO bizcard_details(name, designation, company_name, contact, email, website,
                                                        address, pincode, image)
                                                        
                                                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

            values = (df_4["NAME"].values[0],
                    df_4["DESIGNATION"].values[0],
                    df_4["COMPANY_NAME"].values[0],
                    df_4["CONTACT"].values[0],
                    df_4["EMAIL"].values[0],
                    df_4["WEBSITE"].values[0],
                    df_4["ADDRESS"].values[0],
                    df_4["PINCODE"].values[0],
                    df_4["IMAGE"].values[0])
            cursor.execute(insert_query, values)
            mydb.commit()

            st.success("MODIFIED SUCCESSFULLY")

            
elif select == "Delete":
    st.write("### \U0001F5D1\U0000FE0F You are currently viewing the Delete Section")
    st.write("")
    mydb = psycopg2.connect(host = "localhost",
                                user = "postgres",
                                password = "Charanya@09",
                                database = "bizcard",
                                port = 5432
                                )
    cursor = mydb.cursor()

    col1, col2 = st.columns(2)
    with col1:
        select_query = '''SELECT NAME FROM bizcard_details'''
        cursor.execute(select_query)
        table1 = cursor.fetchall()
        mydb.commit()

        names = []
        for i in table1:
            names.append(i[0]) 
        select_name = st.selectbox("Select the name for Modification", names)

    with col2:
        select_query = f"SELECT DESIGNATION FROM bizcard_details WHERE name = '{select_name}'"
        cursor.execute(select_query)
        table2 = cursor.fetchall()
        mydb.commit()

        designations = []
        for j in table2:
            designations.append(j[0]) 
        select_designation = st.selectbox("Select the designation", designations)
    
    if select_name and select_designation:
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"Selected Name : {select_name}")
            st.write("")
            st.write("")
            st.write("")
            

        with col2:
            st.write(f"Selected Designation : {select_designation}")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
            st.write("")
        
        delete = st.button("Delete", use_container_width = True)

        if delete:
            cursor.execute(f"DELETE FROM bizcard_details WHERE NAME = '{select_name}' AND DESIGNATION = '{select_designation}'")
            mydb.commit()
            st.warning("DELETED")
