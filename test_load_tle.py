from src.ingestion.load_tle import load_tle
lines = load_tle("data/raw/iss.txt")
print(len(lines))
