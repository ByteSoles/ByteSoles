import os
import csv
import django
from catalog.models import Sneaker
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'midterm_project.settings')
django.setup()

csv_file_path = 'dataset/sneakers.csv'

if not os.path.exists(csv_file_path):
    print("CSV file not found.")
    exit()

# Buka file CSV menggunakan csv.DictReader
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    for index, row in enumerate(reader):
        try:
            try:
                # Parsing tanggal release
                release_date = datetime.strptime(row['release'], '%Y-%m-%d').date()
            except (ValueError, TypeError):
                print(f"Invalid release date for row {index}. Skipping.")
                continue

            # Membuat slug
            slug = slugify(f"{row['item']} {row['brand']}")

            # Cek apakah sneaker dengan slug ini sudah ada
            if not Sneaker.objects.filter(slug=slug).exists():
                
                image_url = row['image']
                
                # Cek panjang URL gambar
                if len(image_url) > 200:
                    print(f"Image URL too long for '{row['item']}'. Skipping entry.")
                    continue

                # Membuat objek Sneaker baru
                sneakers = Sneaker(
                    name=row['item'],
                    brand=row['brand'],
                    price=float(row['retail']) if row['retail'] else 0,
                    image=image_url,
                    release_date=release_date,
                    slug=slug,
                )

                try:
                    # Validasi dan simpan data sneaker
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