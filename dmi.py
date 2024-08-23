import streamlit as st
import pandas as pd
import re
from openpyxl import load_workbook

# Load your mapping file from JSON or other formats
# This is a simplified example based on your provided mapping structure.
mapping = {
    "required": "true",
    "properties": {
        "customer": {
            "required": "true",
            "fieldType": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "required": "true",
                    "fieldType": "direct",
                    "availableValues": [
                        "MR",
                        "MRS",
                        "MISS",
                        "M/S"
                    ],
                    "flatFileHeader": "Applicant Title"
                },
                "name": {
                    "type": "string",
                    "required": "true",
                    "flatFileHeader": "Applicant First Name",
                    "pattern": "^[A-Za-z ]*$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "fieldType": "direct"
                },
                "middleName": {
                    "type": "string",
                    "required": "false",
                    "flatFileHeader": "Applicant Middle Name",
                    "pattern": "^[A-Za-z ]*$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "fieldType": "direct"
                },
                "lastName": {
                    "type": "string",
                    "required": "true",
                    "flatFileHeader": "Applicant Last Name",
                    "pattern": "^[A-Za-z ]*$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "fieldType": "direct"
                },
                "gender": {
                    "type": "string",
                    "required": "true",
                    "flatFileHeader": "Applicant Gender",
                    "fieldType": "direct",
                    "availableValues": [
                        "Male",
                        "Female",
                        "Other"
                    ]
                },
                "dateOfBirth": {
                    "type": "string",
                    "required": "true",
                    "flatFileHeader": "Applicant Date of Birth",
                    "fieldType": "direct"
                },
                "primaryMobileNumber": {
                    "type": "string",
                    "flatFileHeader": "Applicant Mobile",
                    "required": "true",
                    "fieldType": "direct"
                },
                "city": {
                    "type": "string",
                    "flatFileHeader": "Applicant City",
                    "pattern": "^[A-Za-z ]*$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "true",
                    "fieldType": "direct"
                },
                "state": {
                    "type": "string",
                    "flatFileHeader": "Applicant State",
                    "required": "true",
                    "fieldType": "direct"
                },
                "country": {
                    "type": "string",
                    "flatFileHeader": "Applicant Country",
                    "required": "true",
                    "fieldType": "direct"
                },
                "panNumber": {
                    "type": "string",
                    "flatFileHeader": "Applicant Pan Number",
                    "required": "true",
                    "fieldType": "direct"
                },
                "education": {
                    "type": "string",
                    "flatFileHeader": "Applicant Education",
                    "required": "true",
                    "fieldType": "direct",
                    "availableValues": [
                        "10th",
                        "12th",
                        "Graduate",
                        "PG",
                        "Professional",
                        "Below Matric",
                        "Illiterate",
                        "Primary School (upto 5th)",
                        "Middle School (upto 8th)",
                        "Other",
                        "HighSchool or Less",
                        "Post Graduate",
                        "Others"
                    ]
                },
                "email": {
                    "type": "string",
                    "flatFileHeader": "Applicant Email",
                    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "true",
                    "fieldType": "direct"
                },
                "pinCode": {
                    "type": "string",
                    "flatFileHeader": "Applicant pinCode",
                    "required": "true",
                    "fieldType": "direct"
                },
                "partnerCustomerId": {
                    "type": "string",
                    "flatFileHeader": "Customer ID",
                    "required": "true",
                    "fieldType": "direct"
                },
                "partnerId": {
                    "type": "string",
                    "flatFileHeader": "Partner ID",
                    "required": "false",
                    "fieldType": "direct"
                },
                "profile": {
                    "type": "string",
                    "flatFileHeader": "Applicant Profile",
                    "required": "false",
                    "fieldType": "direct"
                }
            }
        },
        "coApplicants": {
            "type": "array",
            "required": "true",
            "fieldType": "array",
            "properties": {
                "title": {
                    "type": "string",
                    "required": "true",
                    "flatFileHeader": "Co Applicant Title",
                    "fieldType": "direct",
                    "availableValues": [
                        "MR",
                        "MRS",
                        "MISS",
                        "M/S"
                    ]
                },
                "name": {
                    "type": "string",
                    "flatFileHeader": "Co Applicant First Name",
                    "pattern": "^[A-Za-z ]*$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "true",
                    "fieldType": "direct"
                },
                "middleName": {
                    "type": "string",
                    "flatFileHeader": "Co Applicant middle Name",
                    "pattern": "^[A-Za-z ]*$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "false",
                    "fieldType": "direct"
                },
                "lastName": {
                    "type": "string",
                    "flatFileHeader": "Co Applicant Last Name",
                    "pattern": "^[A-Za-z ]*$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "true",
                    "fieldType": "direct"
                },
                "dateOfBirth": {
                    "type": "string",
                    "flatFileHeader": "Co Applicant Date Of Birth",
                    "required": "true",
                    "fieldType": "direct"
                },
                "education": {
                    "type": "string",
                    "required": "true",
                    "flatFileHeader": "Co Applicant Education",
                    "fieldType": "direct",
                    "availableValues": [
                        "10th",
                        "12th",
                        "Graduate",
                        "PG",
                        "Professional",
                        "Below Matric",
                        "Illiterate",
                        "Primary School (upto 5th)",
                        "Middle School (upto 8th)",
                        "Other",
                        "HighSchool or Less",
                        "Post Graduate",
                        "Others"
                    ]
                },
                "email": {
                    "type": "string",
                    "required": "true",
                    "flatFileHeader": "Co Applicant Email",
                    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "fieldType": "direct"
                },
                "panNumber": {
                    "type": "string",
                    "required": "true",
                    "flatFileHeader": "Co Applicant Pan Number",
                    "pattern": "[A-Z]{3}[P][A-Z]{1}[0-9]{4}[A-Z]{1}",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "fieldType": "direct"
                },
                "gender": {
                    "type": "string",
                    "required": "true",
                    "flatFileHeader": "Co Applicant Gender",
                    "fieldType": "direct",
                    "availableValues": [
                        "Male",
                        "Female",
                        "Other"
                    ]
                }
            }
        },
        "loanApplication": {
            "type": "object",
            "required": "true",
            "fieldType": "object",
            "properties": {
                "loanTenure": {
                    "type": "string",
                    "flatFileHeader": "Loan Tenure",
                    "pattern": "^\\d+$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "true",
                    "fieldType": "direct"
                },
                "purpose": {
                    "type": "string",
                    "flatFileHeader": "Loan Purpose",
                    "pattern": "^[A-Za-z ]*$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "true",
                    "fieldType": "direct"
                },
                "loanAmount": {
                    "type": "string",
                    "flatFileHeader": "Loan Amount",
                    "pattern": "^\\d+(\\.\\d+)?$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "true",
                    "fieldType": "direct"
                },
                "productCode": {
                    "type": "string",
                    "flatFileHeader": "Product Code",
                    "required": "true",
                    "fieldType": "direct"
                },
                "partnerLoanId": {
                    "type": "string",
                    "flatFileHeader": "Partner Loan Id",
                    "required": "true",
                    "fieldType": "direct"
                },
                "normalInterestRate": {
                    "type": "string",
                    "flatFileHeader": "Normal Interest Rate",
                    "required": "true",
                    "pattern": "^\\d+(\\.\\d+)?$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "fieldType": "direct"
                },
                "channelPartnerCode": {
                    "type": "string",
                    "flatFileHeader": "Channel Partner Code",
                    "required": "true",
                    "fieldType": "direct"
                },
                "partnerCustomerId": {
                    "type": "string",
                    "flatFileHeader": "Partner Customer ID",
                    "required": "true",
                    "fieldType": "direct"
                }
            }
        },
        "loanFeeDTO": {
            "required": "true",
            "fieldType": "object",
            "properties": {
                "partnerProcessingFeeAmount": {
                    "type": "string",
                    "flatFileHeader": "Partner Processing Fees Amount",
                    "pattern": "^\\d+(\\.\\d+)?$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "true",
                    "fieldType": "direct"
                },
                "loanAdditionalFeeDetails": {
                    "required": "true",
                    "fieldType": "object",
                    "properties": {
                        "agreementCharges" : {
                            "type": "string",
                            "flatFileHeader": "Partner Agreement Charges",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "required": "true",
                            "fieldType": "direct"
                        }
                    }
                }
            }
        },
        "businessDetails": {
            "required": "true",
            "fieldType": "object",
            "properties": {
                "businessName": {
                    "type": "string",
                    "required": "true",
                    "flatFileHeader": "Business Name",
                    "fieldType": "direct",
                    "pattern": "^\\S+ .+",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ]
                },
                "businessMobileNumber": {
                    "type": "string",
                    "flatFileHeader": "Business Mobile",
                    "pattern": "[6-9][0-9]{9}",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "false",
                    "fieldType": "direct"
                },
                "businessEmailId": {
                    "type": "string",
                    "flatFileHeader": "Business Email",
                    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "false",
                    "fieldType": "direct"
                },
                "businessStartDate": {
                    "type": "string",
                    "flatFileHeader": "Business Start Date",
                    "required": "true",
                    "fieldType": "direct"
                },
                "businessVintage": {
                    "type": "string",
                    "required": "true",
                    "flatFileHeader": "Business Vintage",
                    "pattern": "^\\d+$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "fieldType": "direct"
                },
                "annualIncome": {
                    "type": "string",
                    "flatFileHeader": "Business Annual Income",
                    "pattern": "^\\d+(\\.\\d+)?$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "false",
                    "fieldType": "direct"
                },
                "businessPanNo": {
                    "type": "string",
                    "flatFileHeader": "Business Pan",
                    "pattern": "[A-Z]{3}[P][A-Z]{1}[0-9]{4}[A-Z]{1}",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "false",
                    "fieldType": "direct"
                },
                "businessGstNo": {
                    "type": "string",
                    "flatFileHeader": "Business GST",
                    "required": "false",
                    "fieldType": "direct"
                },
                "industryType": {
                    "type": "string",
                    "flatFileHeader": "Business Sub Industry",
                    "required": "true",
                    "fieldType": "direct",
                    "availableValues": [
                        "Lawn and garden supply outlets, including nurseries",
                        "Men’s, Women’s and Children’s Clothing",
                        "Shoe Stores",
                        "Alterations, Mending, Seamstresses, Tailors",
                        "Women's Clothing",
                        "Sportswear Store",
                        "Saree Shops",
                        "Boutiques",
                        "Clothing Store",
                        "Insurance sales, underwriting and premiums",
                        "Financial Services",
                        "Management, consulting and public relations services",
                        "Schools, Elementary and Secondary",
                        "Hardware, Furniture -supplies, repair, others",
                        "Electronics Sales",
                        "Electronic Repair Shops",
                        "Motion Picture Theaters",
                        "Art Galleries",
                        "Clubs",
                        "Wholesale clubs",
                        "Dance halls, studios and schools",
                        "Financial Services",
                        "Bakeries",
                        "Caterers",
                        "Eating Places and Restaurants",
                        "Freezer and locker meat provisioners",
                        "Government Services",
                        "Drug Stores and Pharmacies, Diagnostic Centers, Optical supplies, other",
                        "Doctor, Dentist, other medical practitioner",
                        "Opticians and Optical Supplies",
                        "Dentists and orthodontists",
                        "Medical and dental laboratories",
                        "Medical services and health practitioners not elsewhere classified",
                        "Hotel, Paying Guest, Hostel",
                        "General Stores",
                        "Grocery Stores, Supermarkets",
                        "Dairy Products Stores",
                        "Music Stores–Musical Instruments",
                        "Sporting Goods Stores",
                        "Books, Office, School Supply and Stationery Stores",
                        "Game, Toy and Hobby Shops",
                        "Photography Studios",
                        "Second Hand Stores, Used Merchandise Stores",
                        "Lighting Stores",
                        "Home Goods Stores",
                        "Mattress Stores",
                        "Candy Stores",
                        "Pet Shops",
                        "Sports and riding apparel shops",
                        "Household appliance shops",
                        "Bookshops",
                        "Camera and photographic supply shops",
                        "Gift, card, novelty and souvenir shops",
                        "Sewing, needlework, fabric and piece goods shops",
                        "Artist supply and craft shops",
                        "Software Services",
                        "Computer network/information services",
                        "Courier Services – Air and Ground, Freight Forwarders",
                        "Travel Agencies and Tour Operators",
                        "Automobile Supplies and parts",
                        "Automobile services",
                        "Petrol Pumps",
                        "Motorcycle Shops and Repairs",
                        "Auto Repair Shops",
                        "Motorcycle shops and dealers",
                        "Automotive body repair shops",
                        "Laundry, dry cleaning services",
                        "Contracted Services",
                        "Laundry, dry cleaning services",
                        "Consulting services",
                        "Marketing services",
                        "Maintenance and rental services",
                        "Government Services",
                        "Print Shops",
                        "Heating, plumbing and air-conditioning contractors",
                        "Electrical contractors",
                        "Speciality cleaning, polishing and sanitation preparations",
                        "Paints, varnishes and supplies",
                        "Laundry, cleaning and garment services",
                        "Exterminating and disinfecting services",
                        "Management, consulting and public relations services",
                        "Professional services not elsewhere classified",
                        "Jewellery, Precious goods/stone, Religious goods, watch/clock etc"
                    ]
                },
                "tradeReferenceNumber": {
                    "type": "string",
                    "flatFileHeader": "Trade Reference Number (UDYAM)",
                    "required": "true",
                    "fieldType": "direct",
                    "pattern": "^UDYAM(-I)?-[A-Z]{2}-\\d{2}-\\d{7}$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ]
                },
                "tradeReferenceType": {
                    "type": "string",
                    "flatFileHeader": "Trade Reference Type (UDYAM)",
                    "required": "true",
                    "fieldType": "direct",
                    "availableValues": [
                        "UDYAM"
                    ]
                },
                "natureOfBusiness": {
                    "type": "string",
                    "flatFileHeader": "Nature Of Business",
                    "required": "false",
                    "fieldType": "direct",
                    "availableValues": [
                        "TRADING",
                        "MANUFACTURING",
                        "SERVICES"
                    ]
                }
            }
        },
        "customerIncomeDetails": {
            "required": "true",
            "fieldType": "object",
            "properties": {
                "agriIncome": {
                    "type": "string",
                    "required": "true",
                    "flatFileHeader": "Household Agricultural Income",
                    "pattern": "^\\d+(\\.\\d+)?$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "fieldType": "direct"
                },
                "additionalData": {
                    "type": "map",
                    "required": "true",
                    "fieldType": "map",
                    "properties": {
                        "businessCostOfProduction": {
                            "type": "string",
                            "flatFileHeader": "Business Cost of Production",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "paymentOfHouseholdDebts": {
                            "type": "string",
                            "flatFileHeader": "Payment of Household Debts",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "required": "false",
                            "fieldType": "direct"
                        },
                        "householdLivestockExpense": {
                            "flatFileHeader": "Household Livestock Expense",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "type": "string",
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "householdLivestockIncome": {
                            "type": "string",
                            "flatFileHeader": "Household Livestock Income",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "businessWaterElectricityExpense": {
                            "type": "string",
                            "required": "true",
                            "flatFileHeader": "Business Water/Electricity Expense",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "fieldType": "direct"
                        },
                        "businessNonFormalLoanInstallment": {
                            "type": "string",
                            "flatFileHeader": "Business Non Formal Loan Installment",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "required": "false",
                            "fieldType": "direct"
                        },
                        "businessTransportFuelExpense": {
                            "type": "string",
                            "flatFileHeader": "Business Transport Fuel Expense",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "householdAnyOtherIncome": {
                            "type": "string",
                            "flatFileHeader": "Household Any Other Income",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "householdSpouseIncome": {
                            "flatFileHeader": "Household Spouse Income",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "type": "string",
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "householdEducationExpense": {
                            "flatFileHeader": "Household Education Income",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "type": "string",
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "businessRentExpense": {
                            "type": "string",
                            "flatFileHeader": "Business Rent Income",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "householdRentIncome": {
                            "flatFileHeader": "Household Rent Income",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "type": "string",
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "householdAnyOtherExpense": {
                            "type": "string",
                            "flatFileHeader": "Household Any Other Expense",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "businessSalesIncome": {
                            "type": "string",
                            "flatFileHeader": "Business Sales Income",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "businessOtherLoanInstallment": {
                            "type": "string",
                            "flatFileHeader": "Business Other Loan Installment",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "required": "false",
                            "fieldType": "direct"
                        },
                        "houseTransportFuelExpense": {
                            "flatFileHeader": "Household Transport Fuel Expense",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "type": "string",
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "businessOtherExpense": {
                            "type": "string",
                            "required": "true",
                            "flatFileHeader": "Business Other Expense",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "fieldType": "direct"
                        },
                        "houseWaterElectricityExpense": {
                            "type": "string",
                            "required": "true",
                            "flatFileHeader": "Household Water/Electricity Expense",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "fieldType": "direct"
                        },
                        "householdRentExpense": {
                            "type": "string",
                            "flatFileHeader": "Household Rent Expense",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "businessCommunication": {
                            "type": "string",
                            "required": "true",
                            "flatFileHeader": "Business Communication",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "fieldType": "direct"
                        },
                        "householdMedicalExpense": {
                            "type": "string",
                            "flatFileHeader": "Household Medical Expense",
                            "required": "true",
                            "pattern": "^\\d+(\\.\\d+)?$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "fieldType": "direct"
                        }
                    }
                }
            }
        },
        "additionalData": {
            "type": "map",
            "required": "true",
            "fieldType": "map",
            "properties": {
                "noOfDependents": {
                    "type": "string",
                    "required": "true",
                    "flatFileHeader": "No of Dependents",
                    "pattern": "^\\d+$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "fieldType": "direct"
                },
                "totalApplicantExperience": {
                    "type": "string",
                    "flatFileHeader": "Total Applicant Experience",
                    "pattern": "^\\d+$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "true",
                    "fieldType": "direct"
                },
                "referenceName": {
                    "type": "string",
                    "flatFileHeader": "Reference Name",
                    "pattern": "^[A-Za-z ]*$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "true",
                    "fieldType": "direct"
                }
            }
        },
        "addressList": {
            "type": "array",
            "required": "true",
            "fieldType": "array",
            "properties": {
                "city": {
                    "type": "string",
                    "flatFileHeader": "Address City",
                    "required": "true",
                    "pattern": "^[A-Za-z ]*$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "fieldType": "direct"
                },
                "state": {
                    "type": "string",
                    "flatFileHeader": "Address State",
                    "pattern": "^[A-Za-z ]*$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "true",
                    "fieldType": "direct"
                },
                "country": {
                    "type": "string",
                    "required": "true",
                    "flatFileHeader": "Address Country",
                    "fieldType": "direct"
                },
                "pincode": {
                    "type": "string",
                    "flatFileHeader": "Address Pincode",
                    "required": "true",
                    "pattern": "^\\d+$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "fieldType": "direct"
                },
                "email": {
                    "type": "string",
                    "flatFileHeader": "Address Email",
                    "pattern": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "false",
                    "fieldType": "direct"
                },
                "stayType": {
                    "type": "string",
                    "flatFileHeader": "Address Stay Type",
                    "required": "true",
                    "fieldType": "direct",
                    "availableValues": [
                        "Owned",
                        "Rented"
                    ]
                },
                "street": {
                    "type": "string",
                    "flatFileHeader": "Address Street",
                    "pattern": "^[A-Za-z0-9 ]+$",
                    "customValidator": [
                        "PATTERN_VALIDATION"
                    ],
                    "required": "true",
                    "fieldType": "direct"
                }
            }
        },
        "cpvRequest": {
            "required": "true",
            "fieldType": "object",
            "properties": {
                "commonCpvDetails": {
                    "required": "true",
                    "fieldType": "object",
                    "properties": {
                        "agentId": {
                            "type": "string",
                            "flatFileHeader": "CPV Agent Id",
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "agentName": {
                            "type": "string",
                            "required": "true",
                            "flatFileHeader": "CPV Agent Name",
                            "fieldType": "direct"
                        },
                        "agentDateTime": {
                            "type": "string",
                            "flatFileHeader": "CPV Date Time",
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "agentContact": {
                            "type": "string",
                            "flatFileHeader": "CPV Agent Contact",
                            "required": "true",
                            "fieldType": "direct"
                        }
                    }
                },
                "individualCpvDetailsList": {
                    "type": "array",
                    "required": "true",
                    "fieldType": "array",
                    "primaryKeyField": "individualType",
                    "customValidator": [
                        "ARRAY_PRIMARY_ELEMENT_BASED_VALIDATION"
                    ],
                    "properties": {
                        "contactNumberOfPersonMet": {
                            "type": "string",
                            "pattern": "^\\d+$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "flatFileHeader": "Contact Number of Person Met",
                            "required": "false",
                            "fieldType": "direct"
                        },
                        "nameOfPersonMet": {
                            "type": "string",
                            "required": "true",
                            "pattern": "^[A-Za-z ]*$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "flatFileHeader": "Name of Person Met",
                            "fieldType": "direct"
                        },
                        "namePlateAddressPlate": {
                            "flatFileHeader": "Name Plate/Address Plate",
                            "type": "string",
                            "required": "true",
                            "availableValues": [
                                "True",
                                "False"
                            ],
                            "fieldType": "direct"
                        },
                        "latitude": {
                            "type": "string",
                            "flatFileHeader": "Latitude",
                            "pattern": "^[0-9]+\\.[0-9]{1,6}$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "longitude": {
                            "type": "string",
                            "flatFileHeader": "Longitude",
                            "pattern": "^[0-9]+\\.[0-9]{1,6}$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "maritalStatus": {
                            "type": "string",
                            "required": "false",
                            "flatFileHeader": "Marital Status",
                            "customValidator": [
                                "ARRAY_PRIMARY_ELEMENT_BASED_VALIDATION"
                            ],
                            "dependentFieldValidation": [
                                {
                                    "key": "",
                                    "source": {
                                        "required": "true",
                                        "pattern": "^[A-Za-z ]*$"
                                    },
                                    "target": {
                                        "individualType": {
                                            "availableValues": [
                                                "APPLICANT", "CO_APPLICANT"
                                            ]
                                        }
                                    }
                                }
                            ],
                            "fieldType": "direct"
                        },
                        "relationshipOfCustomerAndPersonMet": {
                            "type": "string",
                            "flatFileHeader": "Relationship of Customer and Person met",
                            "pattern": "^[A-Za-z ]*$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "yearsAtCurrentResidence": {
                            "type": "string",
                            "flatFileHeader": "years At Current Residence",
                            "pattern": "^\\d+$",
                            "customValidator": [
                                "PATTERN_VALIDATION"
                            ],
                            "required": "true",
                            "fieldType": "direct"
                        },
                        "businessRelocationRisk": {
                            "type": "string",
                            "required": "false",
                            "flatFileHeader": "Business Relocation Risk",
                            "fieldType": "direct",
                            "customValidator": [
                                "ARRAY_PRIMARY_ELEMENT_BASED_VALIDATION"
                            ],
                            "dependentFieldValidation": [
                                {
                                    "key": "",
                                    "source": {
                                        "required": "true",
                                        "availableValues": [
                                            "No risk",
                                            "Low Risk",
                                            "Medium Risk",
                                            "High Risk"
                                        ]
                                    },
                                    "target": {
                                        "individualType": {
                                            "availableValues": [
                                                "ENTITY"
                                            ]
                                        }
                                    }
                                }
                            ]
                        },
                        "businessRecordBookKeeping": {
                            "type": "string",
                            "required": "false",
                            "flatFileHeader": "Business Record Book Keeping",
                            "fieldType": "direct",
                            "customValidator": [
                                "ARRAY_PRIMARY_ELEMENT_BASED_VALIDATION"
                            ],
                            "dependentFieldValidation": [
                                {
                                    "key": "",
                                    "source": {
                                        "required": "true",
                                        "availableValues": [
                                            "All transaction are recorded",
                                            "Few transaction are recorded",
                                            "Very few transaction are recorded",
                                            "Transaction are not recorded at all"
                                        ]
                                    },
                                    "target": {
                                        "individualType": {
                                            "availableValues": [
                                                "ENTITY"
                                            ]
                                        }
                                    }
                                }
                            ]
                        },
                        "marketReputationOfTheBorrower": {
                            "type": "string",
                            "required": "false",
                            "flatFileHeader": "Market Reputation Of Borrower",
                            "fieldType": "direct",
                            "customValidator": [
                                "ARRAY_PRIMARY_ELEMENT_BASED_VALIDATION"
                            ],
                            "dependentFieldValidation": [
                                {
                                    "key": "",
                                    "source": {
                                        "required": "true",
                                        "availableValues": [
                                            "Excellent",
                                            "Good",
                                            "Satisfactory",
                                            "Average",
                                            "Poor"
                                        ]
                                    },
                                    "target": {
                                        "individualType": {
                                            "availableValues": [
                                                "ENTITY"
                                            ]
                                        }
                                    }
                                }
                            ]
                        },
                        "socialReputation": {
                            "type": "string",
                            "flatFileHeader": "Social Reputation",
                            "fieldType": "direct",
                            "customValidator": [
                                "ARRAY_PRIMARY_ELEMENT_BASED_VALIDATION"
                            ],
                            "dependentFieldValidation": [
                                {
                                    "key": "",
                                    "source": {
                                        "required": "true",
                                        "availableValues": [
                                            "Excellent",
                                            "Good",
                                            "Satisfactory",
                                            "Average",
                                            "Poor"
                                        ]
                                    },
                                    "target": {
                                        "individualType": {
                                            "availableValues": [
                                                "APPLICANT",
                                                "CO_APPLICANT"
                                            ]
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }
            }
        }
    }
}

def validate_header(headers):
    expected_headers = {details["flatFileHeader"] for details in mapping.values() if "flatFileHeader" in details}
    missing_headers = expected_headers - set(headers)
    extra_headers = set(headers) - expected_headers
    return missing_headers, extra_headers

def validate_data(df):
    issues = []
    for col, details in mapping.items():
        flat_file_header = details.get("flatFileHeader")
        if flat_file_header:
            if flat_file_header not in df.columns:
                issues.append(f"Missing column '{flat_file_header}'")
                continue
            
            pattern = details.get("pattern")
            if pattern:
                regex = re.compile(pattern)
                invalid_data = df[flat_file_header].apply(lambda x: not regex.match(str(x)))
                if invalid_data.any():
                    invalid_rows = df[invalid_data].index.tolist()
                    issues.append(f"Invalid data in column '{flat_file_header}' at rows: {', '.join(map(str, invalid_rows))}")
            
            # Check for required fields
            if details.get("required") == "true":
                missing_data = df[flat_file_header].isnull() | (df[flat_file_header] == '')
                if missing_data.any():
                    missing_rows = df[missing_data].index.tolist()
                    issues.append(f"Missing required data in column '{flat_file_header}' at rows: {', '.join(map(str, missing_rows))}")
    return issues

def main():
    st.title("Excel Validation App")
    uploaded_file = st.file_uploader("Upload an Excel file", type=["xlsx"])
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            headers = df.columns.tolist()
            
            # Validate headers
            missing_headers, extra_headers = validate_header(headers)
            if missing_headers:
                st.error(f"Missing headers: {', '.join(missing_headers)}")
            if extra_headers:
                st.error(f"Extra headers: {', '.join(extra_headers)}")
            
            # Validate data
            data_issues = validate_data(df)
            if data_issues:
                for issue in data_issues:
                    st.error(issue)
            else:
                st.success("The Excel file is valid!")
        
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
