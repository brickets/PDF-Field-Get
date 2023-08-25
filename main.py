import pypdf
import csv
import os
import datetime
import shutil
import time

script_directory = os.path.dirname(os.path.abspath(__file__))

# Path to your input PDF
pdf_path = script_directory + "\\pdf input"
files = os.listdir(pdf_path)

for file_name in files:
    if file_name.lower().endswith(".pdf"):
        working_path = os.path.join(pdf_path, file_name)
        
        # Open the PDF file
        with open(working_path, "rb") as working_file:
            pdf_reader = pypdf.PdfReader(working_file)
            
            # Get the AcroForm (form fields) from the PDF
            form = pdf_reader.get_fields()
            
            # Create a dictionary to store extracted data
            data = {}
            
            # Loop through each field in the form
            for field in form:
                field_name = field
                field_value = form[field].get("/V", "")
                
                # Add field data to the dictionary
                data[field_name] = field_value

            # Path to your output CSV
            current_datetime = datetime.datetime.now()
            timestamp = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
            csv_path = script_directory + "\\csv output\\output" + timestamp + ".csv"
            
            # Write data to CSV
            with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
                csv_writer = csv.DictWriter(csv_file, fieldnames=form.keys())
                csv_writer.writeheader()
                
                # Write data row
                csv_writer.writerow(data)
                csv_file.close()
                time.sleep(1)

            
        #shutil.move(working_path, script_directory + "\\pdf processed")
        os.rename(working_path, script_directory + "\\pdf processed\\input_csv_" + timestamp + ".pdf")
        print("Processed: " + working_path)

if not files:
    print("No files in pdf input")