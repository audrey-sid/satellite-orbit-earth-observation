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

if __name__ == "__main__":
    # Bounding Box for Kourou Space Centre
    # Format: [longitude_min, latitude_min, longitude_max, latitude_max]
    kourou_bbox = [-52.80, 5.18, -52.60, 5.30]

    print("Searching for Sentinel-2 images over Kourou...")
    results = search_sentinel_images(
        kourou_bbox, 
        date_range="2026-01-01/..",
        max_cloud_cover=10, 
        limit=3
        )

    print(f"Number of images found: {len(results)}\n")

    # Loop through results and print details
    for item in results:
        image_id = item.id
        date_obs = item.datetime.strftime("%Y-%m-%d")
        cloud_pct = item.properties.get("eo:cloud_cover")

        print(f"ID: {image_id}")
        print(f"Acquisition date: {date_obs}")
        print(f"Cloud cover: {cloud_pct:.2f}%\n")