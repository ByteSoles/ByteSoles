import os
import django
import pandas as pd
from catalog.models import Sneaker
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.text import slugify

# Set up Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'midterm_project.settings')
django.setup()

# Path to your CSV file
csv_file_path = 'dataset/sneakers.csv'

# Check if the file exists
if not os.path.exists(csv_file_path):
    print("CSV file not found.")
else:
    # Load the CSV into a DataFrame, skipping bad lines
    df = pd.read_csv(csv_file_path, on_bad_lines='skip')

    for index, row in df.iterrows():
        try:
            # Parse release date safely
            try:
                release_date = datetime.strptime(row['release'], '%Y-%m-%d').date()
            except (ValueError, TypeError):
                print(f"Invalid release date for row {index}. Skipping.")
                continue

            # Generate a slug from the name and brand to ensure uniqueness
            slug = slugify(f"{row['item']} {row['brand']}")

            # Check if the sneaker with the same slug already exists
            if not Sneaker.objects.filter(slug=slug).exists():
                # Handle overly long image URLs by truncating or skipping
                image_url = row['image']
                if len(image_url) > 200:
                    print(f"Image URL too long for '{row['item']}'. Skipping entry.")
                    continue

                # Create and save the sneaker
                sneakers = Sneaker(
                    name=row['item'],
                    brand=row['brand'],
                    price=row['retail'] if not pd.isna(row['retail']) else 0,
                    image=image_url,
                    release_date=release_date,
                    slug=slug,
                )

                try:
                    sneakers.full_clean()  # Validate the instance before saving
                    sneakers.save()
                    print(f"Saved sneaker: {row['item']} by {row['brand']}")
                except ValidationError as e:
                    print(f"Validation error for sneaker '{row['item']}': {e}")
            else:
                print(f"Sneaker '{row['item']}' with slug '{slug}' already exists. Skipping.")

        except Exception as e:
            print(f"Error processing row {index}: {e}")

    print("CSV data has been loaded into the Django database.")