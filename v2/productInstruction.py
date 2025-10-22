LabSegmentationIntstruction = '''

The columns in the DB can be described by the following definitions; 

Diaceutics Laboratory ID : 	Unique Diaceutics code associated with laboratory
Diaceutics Assay ID	 : Unique Diaceutics code associated with assay
Laboratory Name : 	"Current operating name of the laboratory. Please note each assay offered by a laboratory has a unique row in the excel file. As such, if the laboratory offers more than one assay of interest (i.e., biomarker, disease indication, method), then the laboratory will be listed multiple times."
Street : Laboratory address. Where the laboratory is part of a network, this is the address of the headquarters.
City : Laboratory address. Where the laboratory is part of a network, this is the address of the headquarters.
Laboratory Typ : "This is determined by Diaceutics based upon how the laboratory describes itself on their website: 
    - Academic - Associated with higher learning institutions or operating with research purposes. 
    - Hospital - Associated with a non-academic patient treatment facility, typically located in the community setting
    - Commercial - Not associated with the government and is privately owned/funded"
State :	Laboratory address. Where the laboratory is part of a network, this is the address of the headquarters.
ZIP Code : 	Laboratory address. Where the laboratory is part of a network, this is the address of the headquarters.
Oct'20 - Sep'21 Diaceutics Relative mNSCLC patient market share : "Metastatic NSCLC patient market share based on volume of metastatic NSCLC cancer patients, per lab. This data is from the Diaceutics Data Repository within October 2020 - September 2021 timepoint and is made up of claims data from both Medicare and commercial payers.
    - Metastatic patients are identified as those patients who are either:
        1. Receiving testing which is only associated with a metastatic setting
        2. Have a secondary, metastatic diagnosis
        3. Receiving treatment which is only associated with a metastatic setting
    - The top 100 labs have been profiled for PD-L1 testing capabilities, ranked based on mNSCLC PD-L1 tested patient market share."
Oct'20 - Sep'21 Diaceutics Relative mNSCLC PD-L1 tested patient market share : "Metastatic NSCLC PD-L1 tested patient market share based on the volume of PD-L1 tested patients per lab. This data is from the Diaceutics Data Repository within October 2020 - September 2021 timepoint and is made up of claims data from both Medicare and commercial payers.
    - The top 100 labs have been profiled for PD-L1 testing capabilities, ranked based on mNSCLC PD-L1 tested patient market share."
Laboratory offers PD-L1 testing in NSCLC : "States whether the laboratory offers clinical PD-L1 testing that is advertised for either NSCLC or for 'all solid tumors', as the assumption has been made that a physician could order this test for their NSCLC patients. Any other indication falls outside the scope of this project and hasn't been captured within this excel.
    - Please note: this data is captured at a laboratory level and not at an assay level."
PD-L1 assay offered in-house or send-out? : "States whether the PD-L1 assay is performed:
    - In-house: within their laboratory
    - Send-out: sent to another laboratory to be performed
    - Where a laboratory offers multiple PD-L1 assays for NSCLC, this laboratory will be listed multiple times within this excel.
    - Please note: this data is captured at an assay level and not at a laboratory level."
Name of the send-out laboratory : 	"Name of the send-out laboratory
    - Please note: this data is captured at an assay level and not at a laboratory level."
Name of the PD-L1 assay : "Name of the assay as advertised by the laboratory on their website.
    - Please note: this data is captured at an assay level and not at a laboratory level."
IHC platform(s) used specifically for the assay : "States which IHC platform is the PD-L1 assay being performed on.
    - Please note: this data is captured at an assay level and not at a laboratory level."
Specimen type(s) accepted for testing : "All specimen (sample) types accepted by the laboratory for testing that assay
    - Please note: this data is captured at an assay level and not at a laboratory level."
Classification : "States whether PD-L1 testing is performed using a:
    - Commercial Assay: Laboratory is purchasing a kit from a commercial vendor. This kit could be purchased and performed under the same conditions as multiple labs within that market. This includes Research Use Only/RUO and FDA approved kits.
    - Lab developed test (LDT): A test that is developed and validated for use in-house which cannot be purchased from a commercial vendor. LDTs are typically unique to that specific laboratory (i.e. test quality is variable amongst labs using LDTs therefore there is high importance on participation in EQA programs)
    - Please note: this data is captured at an assay level and not at a laboratory level."
Commercial assay name :	"Name of the commercial assay offered by the laboratory
    - This data is captured at an assay level and not at a laboratory level."
Regulatory status :	"Regulatory status of the commercial assay being used (i.e., FDA approved, Research Use Only/RUO).
    - This data is captured at an assay level and not at a laboratory level."
Laboratory turnaround time (days) : "Laboratory turnaround time of the assay, in days.
    - This turnaround time reflects the time taken from the sample being received into the laboratory until a result is reported back to the requesting clinician.
    - This data is captured at an assay level and not at a laboratory level."
Laboratory has access to a Dako Omnis platform?" : "States whether the laboratory has access to a Dako Omnis platform, even if PD-L1 testing isn't currently being performed on the platform. Where a laboratory is offering PD-L1 testing as a send-out, access to Dako Omnis may still be captured as the laboratory may offer in-house IHC testing testing for other biomarkers.
    - Please note: this data is captured at a laboratory level and not at an assay level."
IHC platforms available within the laboratory (where available)" : "States which IHC platform(s) are available within the laboratory, even if PD-L1 testing isn't currently being performed on the platform. Where a laboratory is offering PD-L1 testing as a send-out, IHC platforms may still be captured as the laboratory may offer in-house IHC testing for other biomarkers.
    - Please note: this data is captured at a laboratory level and not at an assay level."

'''

product_instructions = {
    "labSegmentation": LabSegmentationIntstruction
}