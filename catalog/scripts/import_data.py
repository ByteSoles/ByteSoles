import os
import django
import pandas as pd
from catalog.models import Sneaker
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'midterm_project.settings')
django.setup()

def run(): 

    csv_file_path = 'dataset/sneakers.csv'

    if not os.path.exists(csv_file_path):
        print("CSV file not found.")
        return

    df = pd.read_csv(csv_file_path, on_bad_lines='skip')

    for index, row in df.iterrows():
        
        try:
            try:
                release_date = datetime.strptime(row['release'], '%Y-%m-%d').date()
            except (ValueError, TypeError):
                print(f"Invalid release date for row {index}. Skipping.")
                continue

            slug = slugify(f"{row['item']} {row['brand']}")

            if not Sneaker.objects.filter(slug=slug).exists():
                
                image_url = row['image']
                if len(image_url) > 200:
                    print(f"Image URL too long for '{row['item']}'. Skipping entry.")
                    continue

                sneakers = Sneaker(
                    name=row['item'],
                    brand=row['brand'],
                    price=row['retail'] if not pd.isna(row['retail']) else 0,
                    image=image_url,
                    release_date=release_date,
                    slug=slug,
                )

                try:
                    sneakers.full_clean()  
                    sneakers.save()
                    print(f"Saved sneaker: {row['item']} by {row['brand']}")
                except ValidationError as e:
                    print(f"Validation error for sneaker '{row['item']}': {e}")
            else:
                print(f"Sneaker '{row['item']}' with slug '{slug}' already exists. Skipping.")

        except Exception as e:
            print(f"Error processing row {index}: {e}")

    print("CSV data has been loaded into the Django database.")