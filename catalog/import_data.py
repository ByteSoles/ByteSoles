import os
import django
import pandas as pd
from catalog.models import Sneaker  # Adjust with your app name
from django.utils.text import slugify
from datetime import datetime
from django.conf import settings

# Set the settings module for the Django project
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'midterm_project.settings')

# Initialize Django
django.setup()

# Read CSV file into a DataFrame
csv_file_path = 'dataset/sneakers.csv'

# Check if the file exists
if os.path.exists(csv_file_path):
    print("File exists!")
else:
    print("File not found.")

# Read the CSV file
df = pd.read_csv(csv_file_path, on_bad_lines='skip')

# Function to generate unique slugs
def generate_unique_slug(name):
    slug = slugify(name)
    counter = 1
    # Ensure the slug is unique
    while Sneaker.objects.filter(slug=slug).exists():
        slug = f"{slug}-{counter}"
        counter += 1
    return slug

for index, row in df.iterrows():
    release_date = datetime.strptime(row['release'], '%Y-%m-%d').date()

    # Check if the sneaker already exists based on 'name' and 'brand'
    if not Sneaker.objects.filter(name=row['item'], brand=row['brand']).exists():
        # Generate slug
        slug = generate_unique_slug(row['item'])

        # Create the Sneaker instance
        sneakers = Sneaker(
            name=row['item'],
            brand=row['brand'],
            price=row['retail'],
            image=row['image'],
            release_date=release_date,
            slug=slug,
        )
        
        # Save the Sneaker instance to the database
        sneakers.save()
    else:
        print(f"Sneaker '{row['item']}' by {row['brand']} already exists. Skipping.")

print("CSV data has been loaded into the Django database.")
