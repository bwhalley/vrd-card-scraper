import csv

# Open input CSV file
with open('cards.csv', 'r') as input_file:
    csv_reader = csv.DictReader(input_file)
    
    # Open output CSV file
    with open('vrd.csv', 'w', newline='') as output_file:
        csv_writer = csv.writer(output_file)
        
        # Write header
        csv_writer.writerow(['name'])
        
        # Extract and write names
        for row in csv_reader:
            csv_writer.writerow([row['name']])
