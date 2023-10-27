import xml.etree.ElementTree as ET

FILE = 'installationdocs/IF_installation.xml'

# Load the XML file
tree = ET.parse(FILE)
root = tree.getroot()

# Define a list of tags to remove
tags_to_remove = ['entry', 'dcequivalent', 'repeatable', 'modality', 'guideline', 'example']

# Iterate over metadataElement elements
for metadata_element in root.findall('.//metadataElement/labels/label'):
    # Iterate over the specified tags and remove them
    for tag_name in tags_to_remove:
        tag = metadata_element.find(tag_name)
        if tag is not None:
            metadata_element.remove(tag)

# Save the modified XML back to a file
tree.write(FILE, encoding='utf-8', xml_declaration=True)

print("Tags removed successfully.")
