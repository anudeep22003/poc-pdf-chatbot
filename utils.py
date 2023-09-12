def metadata_for_doc_id(filename: str):
    if filename == "data/IFU_CEREC_Primemill_EN_6719681.pdf":
        return {
            "purpose": "This device is used for computed-aided production of dental restorations, abutments, parts of abutments and drilling templates for implant placement.",
            "modelname": "CEREC Primemill",
            "manufacturer": "Dentsply Sirona",
        }
    if filename == "data/IFU_Primescan_Connect.pdf":
        return {
            "purpose": "Primescan Connect allows you to send digital scans to a laboratory of your choice for manufacture at your laboratory partner.",
            "modelname": "Primescan Connect",
            "manufacturer": "Dentsply Sirona",
        }
    if filename == "data/OM_CEREC_SW_5.pdf":
        return {
            "purpose": "When combined with the CEREC acquisition unit and a production unit, the software enables computer-assisted manufacturing of dental restorations, e.g. from ceramic material with a natural appearance.",
            "modelname": "CEREC SW 5",
            "manufacturer": "Dentsply Sirona",
        }


documents_to_index = [
    ("IFU_CEREC_Primemill.pdf", 5, 3),
    ("IFU_Primescan_Connect.pdf", 4, 5),
    ("OM_CEREC_SW_5.pdf", 8, 4),
    ("IFU_Primescan_Connect_DE.pdf", 4, 5),
]
