# Author: Özge Çinko
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
from geopy.geocoders import Nominatim


def get_exif_data(image):
    """Extracts EXIF data from the given image file."""
    exif_data = {}
    try:
        with Image.open(image) as img:
            info = img._getexif()
            for tag, value in info.items():
                decoded_tag = TAGS.get(tag, tag)
                if decoded_tag == 'GPSInfo':
                    gps_data = {}
                    for gps_tag in value:
                        sub_decoded_tag = GPSTAGS.get(gps_tag, gps_tag)
                        gps_data[sub_decoded_tag] = value[gps_tag]
                    exif_data[decoded_tag] = gps_data
                else:
                    exif_data[decoded_tag] = value
    except (IOError, AttributeError, KeyError, IndexError) as err:
        print("Error: ", err)
    return exif_data


def print_exif_data(exif_data):
    for tag, value in exif_data.items():
        print(f"{tag}: {value}")


exif_data = get_exif_data('image.jpeg')
print_exif_data(exif_data)


def dms_to_decimal(degrees, minutes, seconds, direction):
    """Converts GPS coordinates in degrees, minutes, and seconds format to decimal degrees."""
    decimal_degrees = float(degrees) + (float(minutes) / 60) + (float(seconds) / 3600)
    if direction in ['S', 'W']:
        decimal_degrees *= -1
    return decimal_degrees


def get_location_address(exif_data):
    geolocator = Nominatim(user_agent="metadata/1.0")

    lat_deg, lat_min, lat_sec = exif_data["GPSInfo"]["GPSLatitude"]
    lat_dir = exif_data["GPSInfo"]["GPSLatitudeRef"]
    lon_deg, lon_min, lon_sec = exif_data["GPSInfo"]["GPSLongitude"]
    lon_dir = exif_data["GPSInfo"]["GPSLongitudeRef"]

    lat = dms_to_decimal(lat_deg, lat_min, lat_sec, lat_dir)
    lon = dms_to_decimal(lon_deg, lon_min, lon_sec, lon_dir)

    location = geolocator.reverse(f"{lat}, {lon}")

    print("Location Address: ", location.address)


get_location_address(exif_data)
