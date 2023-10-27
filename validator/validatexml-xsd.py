from lxml import etree

# Load the XML file
xml_file = input("Include the path to your xml file: ")
xsd_file = input("Include your path to your xsd schema: ")

# Parse the XML and XSD files
xml_doc = etree.parse(xml_file)
xsd_doc = etree.parse(xsd_file)

# Create a schema object
xmlschema = etree.XMLSchema(xsd_doc)

# Validate the XML against the XSD
is_valid = xmlschema.validate(xml_doc)

if is_valid:
    print("XML is valid against the XSD.")
else:
    print("XML is not valid against the XSD.")
    # If the XML is not valid, you can print validation errors
    for error in xmlschema.error_log:
        print(error)
