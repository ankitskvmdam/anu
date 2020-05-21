# import xml.etree.ElementTree as ET
# from lxml import etree as ET

# location = "./raw/test.mif25"
# test_location = "./test.xml"

# parser = ET.XMLParser(remove_blank_text=True)
# dom = ET.parse(location, parser)

# # print(ET.tostring(dom))
# ns = {"mif": "http://psi.hupo.org/mi/mif"}

# entry_list = dom.xpath("//mif:entry", namespaces=ns)

# first_entry = entry_list[0]

# first_interactor_list = first_entry.xpath("//mif:interactorList", namespaces=ns)

# first_interactor = first_interactor_list[0].xpath("//mif:interactor", namespaces=ns)

# root = first_interactor[0]

# print(root.attrib, root.text)
# for child in root:
#     print(child.tag, child.attrib, child.text)

# for child in first_entry:
#     print(child.tag, child.attrib, child.text)

# for child in first_interactor_list:
#     print(child.tag, child.attrib, child.text)


"""mif25 parser so that it can be processed by pandas dataframe."""
from lxml import etree as ET
from typing import List, TypedDict


class Xref(TypedDict):
    """Dictionary shape for xref."""

    id: str
    db: str
    dbAc: str
    refType: str
    refTypeAc: str


class FileDict(TypedDict):
    """Shape of dictionary which will be return by parser."""

    interactor_id: List[str]
    short_label: List[str]
    fullname: List[str]
    xref: List[List[Xref]]
    interactor_type: List[str]
    interactor_type_xref: List[List[Xref]]
    organism_ncbi_tax_id: List[str]
    organism_short_label: List[str]
    organism_fullname: List[str]


class Mif25Parser:
    """mif25 parser class."""

    def __init__(self: "Mif25Parser") -> None:
        """Initialize Mif25Parser instance."""
        self.namespace = {"mif": "http://psi.hupo.org/mi/mif"}
        self.file_dict: FileDict = {
            "interactor_id": [],
            "short_label": [],
            "fullname": [],
            "xref": [[]],
            "interactor_type": [],
            "interactor_type_xref": [[]],
            "organism_ncbi_tax_id": [],
            "organism_short_label": [],
            "organism_fullname": [],
        }

    def get_xpath_list(self: "Mif25Parser", xml: ET.ElementTree, query: str) -> None:
        """Return the list of node satisfy query."""
        return xml.xpath(query, namespaces=self.namespace)

    def add_interactor_id(self: "Mif25Parser", id_dict: {"id": str}) -> None:
        """Add interactor id to file_dict."""
        self.file_dict.interactor_id.append(id_dict["id"])

    def parse(self: "Mif25Parser", path: str) -> None:
        """Parse the mif25 file.

        Args:
            path: path of the mif25 file.
        """

        xml_parser = ET.XMLParser(remove_blank_text=True)
        xml = ET.parse(path, xml_parser)

        # Currently, assuming there is only one entry node and interactor list node.
        entry_list = self.get_xpath_list(xml, "//mif:entry")
        interactor_list_list = self.get_xpath_list(
            entry_list[0], "//mif:interactorList"
        )

        interactors = self.get_xpath_list(interactor_list_list[0], "//mif:interactor")

        for interactor in interactors:
            # self.add_interactor_id(interactor.attrib["id"])
            names = self.get_xpath_list(interactor, "//mif:names")[0]
            xref = self.get_xpath_list(interactor, "//mif:xref")[0]
            interactor_type = self.get_xpath_list(interactor, "//mif:interactorType")[0]
            orgnamism = self.get_xpath_list(interactor, "//mif:organism")[0]

            for child in names:
                print(child.tag, child.text)
            break


parser = Mif25Parser()
location = "./raw/test.mif25"

parser.parse(location)
