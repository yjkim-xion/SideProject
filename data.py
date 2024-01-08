import os
import django
import csv
from cars.models import Car, Version

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


def import_csv(csv_file_path):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            car = Car(
                name=row['name'],
                brand=row['brand'],
                vin=row['vin'],
                price=row['price'],
                is_sold=row['is_sold'] == 'False'
            )
            car.save()

            versions = int(row['version']) if row['version'] else None
            version_price = int(row['price']) if row['price'] else 0
            if versions is not None:
                version = Version(car=car, versions=versions, price=version_price)
                version.save()


if __name__ == "__main__":
    import_csv("C:/Users/Kim/Downloads/MOCK_DATA (8).csv")
