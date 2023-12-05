import csv


def write_to_csv(call_details):
    # Define the CSV file name
    csv_file = 'call_details.csv'

    # Define the fieldnames for the CSV
    fieldnames = ['call_id', 'status', 'phone_from', 'phone_to']

    # Check if the file already exists, if not, write the header row
    with open(csv_file, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:
            writer.writeheader()

        # Write the call details to the CSV
        writer.writerow(call_details)
