import requests
from pystac_client import Client

# Search Sentinel-2 images using the STAC API
def search_sentinel_images(bbox, date_range="2026-01-01/..", max_cloud_cover=10, limit=3):
    # URL of the open-data STAC catalog
    client = Client.open("https://earth-search.aws.element84.com/v1")

    # Search in sentinel-2-l2a collection with cloud filter
    search_query = client.search(
        collections=["sentinel-2-l2a"],
        bbox=bbox,
        datetime = date_range,
        query={"eo:cloud_cover": {"lt": max_cloud_cover}},
        limit=limit,
    )

    # Convert search results to a Python list
    items = list(search_query.items())
    return items[:limit]

# Download the RGB preview image
def download_preview_image(item, output_path="data/raw/sentinel_kourou.jpg"):
    # Get preview image URL
    preview_asset = item.assets.get("rendered_preview") or item.assets.get(
        "thumbnail")

    if preview_asset:
        preview_url = preview_asset.href
        print(f"Downloading: {preview_url}")
        response = requests.get(preview_url)

        # Save image if download is successful
        if response.status_code == 200:
            with open(output_path, "wb") as file:
                file.write(response.content)
            print(f"Saved: {output_path}")
        else:
            print(f"Error HTTP: {response.status_code}")
    else:
        print("No preview found.")

if __name__ == "__main__":
    # Bounding Box for Kourou Space Centre
    # Format: [longitude_min, latitude_min, longitude_max, latitude_max]
    ariane6_bbox = [-52.791, 5.251, -52.781, 5.261]

    print("Searching images...")
    results = search_sentinel_images(
        ariane6_bbox, 
        date_range="2026-01-01/..",
        max_cloud_cover=10, 
        limit=3
        )

    print(f"Found: {len(results)}\n")

    # If images are found, select the first one and download its preview
    if results:
        best_image = results[0]
        print(f"Selected: {best_image.id}")
        print(f"Date: {best_image.datetime.strftime('%Y-%m-%d')}\n")

        download_preview_image(best_image, "data/raw/sentinel_kourou.jpg")