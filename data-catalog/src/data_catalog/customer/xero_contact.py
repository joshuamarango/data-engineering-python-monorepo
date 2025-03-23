from pydantic import BaseModel, ConfigDict, Field, GenerateSchema
from typing import List, Optional

from data_catalog.json_schema import GlueSchemaGenerator


class XeroAddress(BaseModel):
    addressType: Optional[str] = Field(None, alias="AddressType")
    addressLine1: Optional[str] = Field(None, alias="AddressLine1")
    city: Optional[str] = Field(None, alias="City")
    postalCode: Optional[str] = Field(None, alias="PostalCode")
    attentionTo: Optional[str] = Field(None, alias="AttentionTo")


class XeroPhone(BaseModel):
    phoneType: Optional[str] = Field(None, alias="PhoneType")
    phoneNumber: Optional[str] = Field(None, alias="PhoneNumber")
    phoneAreaCode: Optional[str] = Field(None, alias="PhoneAreaCode")
    phoneCountryCode: Optional[str] = Field(None, alias="PhoneCountryCode")


class XeroContact(BaseModel):
    """
    Represents a contact in Xero.
    """

    model_config = ConfigDict(
        title="xeroContact",
        json_schema_mode_override="serialization",
        schema_generator=GlueSchemaGenerator(description="A contact record from Xero representing either a customer or supplier, containing their contact details, addresses, tax information and other metadata."),
    )

    contactId: str = Field(..., alias="ContactID")
    contactStatus: str = Field(..., alias="ContactStatus")
    name: str = Field(..., alias="Name")
    firstName: Optional[str] = Field(None, alias="FirstName")
    lastName: Optional[str] = Field(None, alias="LastName")
    companyNumber: Optional[str] = Field(None, alias="CompanyNumber")
    emailAddress: Optional[str] = Field(None, alias="EmailAddress")
    bankAccountDetails: Optional[str] = Field(None, alias="BankAccountDetails")
    taxNumber: Optional[str] = Field(None, alias="TaxNumber")
    accountsReceivableTaxType: Optional[str] = Field(None, alias="AccountsReceivableTaxType")
    accountsPayableTaxType: Optional[str] = Field(None, alias="AccountsPayableTaxType")
    addresses: Optional[List[XeroAddress]] = Field(None, alias="Addresses")
    phones: Optional[List[XeroPhone]] = Field(None, alias="Phones")
    updatedDateUTC: Optional[str] = Field(None, alias="UpdatedDateUTC")
    isSupplier: Optional[bool] = Field(None, alias="IsSupplier")
    isCustomer: Optional[bool] = Field(None, alias="IsCustomer")
    defaultCurrency: Optional[str] = Field(None, alias="DefaultCurrency")
