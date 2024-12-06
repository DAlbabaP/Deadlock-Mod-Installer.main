import json
import pandas as pd
import os

def json_to_excel():
    # Read JSON file
    with open('descriptions.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Convert to list of dictionaries
    rows = []
    for item_name, item_data in data.items():
        row = {
            'Name': item_name,
            'Title': item_data['title'].replace('# ', ''),
            'Author': item_data['author'],
            'Last Updated': item_data['last_updated'],
            'Preview Image': item_data['media'].get('preview', ''),
            'Video': item_data['media'].get('video', ''),
            'Description EN': item_data['descriptions'].get('en', ''),
            'Description RU': item_data['descriptions'].get('ru', '')
        }
        rows.append(row)

    # Create DataFrame and sort by Name
    df = pd.DataFrame(rows)
    df = df.sort_values('Name')

    # Save to Excel
    df.to_excel('descriptions_edit.xlsx', index=False)
    print('Created Excel file: descriptions_edit.xlsx')
    print('You can now edit the Excel file. When done, run this script again.')

def excel_to_json():
    # Read Excel file
    df = pd.read_excel('descriptions_edit.xlsx')
    
    # Convert back to JSON structure
    data = {}
    for _, row in df.iterrows():
        data[row['Name']] = {
            'title': f"# {row['Title']}",
            'author': row['Author'],
            'last_updated': row['Last Updated'],
            'media': {
                'preview': row['Preview Image'] if pd.notna(row['Preview Image']) else '',
                'video': row['Video'] if pd.notna(row['Video']) else None
            },
            'descriptions': {
                'en': row['Description EN'] if pd.notna(row['Description EN']) else '',
                'ru': row['Description RU'] if pd.notna(row['Description RU']) else ''
            }
        }

    # Save back to JSON
    with open('descriptions_new.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print('Created new JSON file: descriptions_new.json')

def main():
    if not os.path.exists('descriptions_edit.xlsx'):
        json_to_excel()
    else:
        excel_to_json()

if __name__ == '__main__':
    main()
