import csv
import json
import ast

def convert_python_to_json(row):
    try:
        # Use ast.literal_eval to safely convert Python string to dict
        python_dict = ast.literal_eval(row)
        
        # Handle None values (Python None -> JSON null)
        def convert_none(obj):
            if isinstance(obj, dict):
                return {k: convert_none(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_none(item) for item in obj]
            elif obj is None:
                return None
            return obj
        
        return convert_none(python_dict)
    except Exception as e:
        print(f"Error converting row: {row[:100]}...")
        print(f"Error: {str(e)}")
        return None

def process_csv():
    records = []
    
    with open('results.csv', 'r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            try:
                if len(row) > 0:  # Make sure we have data
                    json_data = convert_python_to_json(row[0])
                    if json_data:
                        records.append(json_data)
            except Exception as e:
                print(f"Error processing row: {row[:100]}...")
                print(f"Error: {str(e)}")
                continue
    
    # Write valid JSON array to file
    with open('fixed_results.json', 'w') as file:
        json.dump(records, file, indent=2)
    
    print(f"Successfully processed {len(records)} records")

if __name__ == "__main__":
    process_csv() 