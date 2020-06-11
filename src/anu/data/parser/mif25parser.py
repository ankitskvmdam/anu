"""mif25 parser so that it can be processed by pandas dataframe."""

from typing import List, TypedDict

from lxml import etree as ET  # type: ignore


class Xref(TypedDict):
    """Dictionary shape for xref."""

    id: str
    db: str
    dbAc: str
    refType: str
    refTypeAc: str


class Name(TypedDict):
    """Dictionary shape for name."""

    short_label: str
    fullname: str


class FileDict(TypedDict):
    """Shape of dictionary which will be return by parser."""

    interactor_id: List[str]
    short_label: List[str]
    fullname: List[str]
    xref: List[List[Xref]]
    interactor_type_fullname: List[str]
    interactor_type_short_label: List[str]
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
            "xref": [],
            "interactor_type_fullname": [],
            "interactor_type_short_label": [],
            "interactor_type_xref": [],
            "organism_ncbi_tax_id": [],
            "organism_short_label": [],
            "organism_fullname": [],
        }

    def get_xpath_list(
        self: "Mif25Parser", xml: ET.ElementTree, query: str
    ) -> ET.ElementTree:
        """Return the list of node satisfy query."""
        return xml.xpath(query, namespaces=self.namespace)

    def process_name(self: "Mif25Parser", names: ET.ElementTree) -> Name:
        """Process names element tree"""
        name: Name = {"short_label": "", "fullname": ""}

        short_label = self.get_xpath_list(names, "./mif:shortLabel")
        fullname = self.get_xpath_list(names, "./mif:fullName")

        if len(short_label) != 0:
            short_label = short_label[0].text
        else:
            short_label = ""

        if len(fullname) != 0:
            fullname = fullname[0].text
        else:
            fullname = ""

        name["short_label"] = short_label
        name["fullname"] = fullname

        return name

    def process_xref(self: "Mif25Parser", xrefs: ET.ElementTree) -> List[Xref]:
        """Process xref."""
        primary_ref = self.get_xpath_list(xrefs, "./mif:primaryRef")[0]
        secondary_refs = self.get_xpath_list(xrefs, "./mif:secondaryRef")

        xref_list: List[Xref] = [primary_ref.attrib]

        for ref in secondary_refs:
            xref_list.append(ref.attrib)

        return xref_list

    def process_interactor_type(
        self: "Mif25Parser", interactor_type: ET.ElementTree
    ) -> None:
        """Process interactor type dom."""
        names = self.get_xpath_list(interactor_type, "./mif:names")[0]
        xrefs = self.get_xpath_list(interactor_type, "./mif:xref")[0]

        name = self.process_name(names)
        xref_list = self.process_xref(xrefs)

        self.file_dict["interactor_type_short_label"].append(name["short_label"])
        self.file_dict["interactor_type_fullname"].append(name["fullname"])
        self.file_dict["interactor_type_xref"].append(xref_list)

    def process_organism(self: "Mif25Parser", organism: ET.ElementTree) -> None:
        """Process organism type dom."""
        names = self.get_xpath_list(organism, "./mif:names")[0]

        name = self.process_name(names)

        self.file_dict["organism_short_label"].append(name["short_label"])
        self.file_dict["organism_fullname"].append(name["fullname"])
        self.file_dict["organism_ncbi_tax_id"].append(organism.attrib["ncbiTaxId"])

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
            entry_list[0], "./mif:interactorList"
        )

        interactors = self.get_xpath_list(interactor_list_list[0], "./mif:interactor")

        for interactor in interactors:
            names = self.get_xpath_list(interactor, "./mif:names")[0]
            xrefs = self.get_xpath_list(interactor, "./mif:xref")[0]
            interactor_type = self.get_xpath_list(interactor, "./mif:interactorType")[0]
            organism = self.get_xpath_list(interactor, "./mif:organism")[0]

            name = self.process_name(names)
            xref_list = self.process_xref(xrefs)

            self.file_dict["interactor_id"].append(interactor.attrib["id"])
            self.file_dict["short_label"].append(name["short_label"])
            self.file_dict["fullname"].append(name["fullname"])
            self.file_dict["xref"].append(xref_list)
            self.process_interactor_type(interactor_type)
            self.process_organism(organism)
