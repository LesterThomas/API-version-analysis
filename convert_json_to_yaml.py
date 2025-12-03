import json
import yaml

# Read JSON file
with open(
    "TMF620_Product_Catalog_Management_API_v4.1.0_swagger.json", "r", encoding="utf-8"
) as json_file:
    data = json.load(json_file)

# Write YAML file
with open(
    "TMF620_Product_Catalog_Management_API_v4.1.0_swagger.yaml", "w", encoding="utf-8"
) as yaml_file:
    yaml.dump(
        data, yaml_file, default_flow_style=False, allow_unicode=True, sort_keys=False
    )

print("Conversion completed successfully!")
