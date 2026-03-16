import h3


def generate_kml(records):
    kml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<kml xmlns="http://www.opengis.net/kml/2.2">',
        "<Document>",
        """
        <Schema name="cell_schema" id="cell_schema">
            <SimpleField name="level" type="int"/>
            <SimpleField name="cell_id" type="int"/>
        </Schema>
        """,
    ]

    for rec in records:
        boundary = h3.cell_to_boundary(rec.h3_index)
        coords = " ".join(f"{lng},{lat},0" for lat, lng in boundary)

        kml.append(
            f"""
            <Placemark>
              <name>{rec.h3_index}</name>

              <ExtendedData>
                <SchemaData schemaUrl="#cell_schema">
                  <SimpleData name="level">{rec.level}</SimpleData>
                  <SimpleData name="cell_id">{rec.cell_id}</SimpleData>
                </SchemaData>
              </ExtendedData>

              <Polygon>
                <outerBoundaryIs>
                  <LinearRing>
                    <coordinates>
                    {coords}
                    </coordinates>
                  </LinearRing>
                </outerBoundaryIs>
              </Polygon>
            </Placemark>
            """
        )

    kml.append("</Document></kml>")
    return "\n".join(kml)
