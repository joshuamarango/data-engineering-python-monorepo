from pydantic import BaseModel, ConfigDict, Field, GenerateSchema
from typing import List, Optional

from data_catalog.json_schema import GlueSchemaGenerator


class XeroInvoiceContact(BaseModel):
    contactId: Optional[str] = Field(None, alias="ContactID")
    contactStatus: Optional[str] = Field(None, alias="ContactStatus")
    name: Optional[str] = Field(None, alias="Name")
    addresses: Optional[List["XeroAddress"]] = Field(None, alias="Addresses")
    phones: Optional[List["XeroPhone"]] = Field(None, alias="Phones")
    updatedDateUTC: Optional[str] = Field(None, alias="UpdatedDateUTC")
    isSupplier: Optional[str] = Field(None, alias="IsSupplier")
    isCustomer: Optional[str] = Field(None, alias="IsCustomer")


class XeroAddress(BaseModel):
    addressType: Optional[str] = Field(None, alias="AddressType")
    addressLine1: Optional[str] = Field(None, alias="AddressLine1")
    addressLine2: Optional[str] = Field(None, alias="AddressLine2")
    city: Optional[str] = Field(None, alias="City")
    postalCode: Optional[str] = Field(None, alias="PostalCode")


class XeroPhone(BaseModel):
    phoneType: Optional[str] = Field(None, alias="PhoneType")
    phoneNumber: Optional[str] = Field(None, alias="PhoneNumber")
    phoneAreaCode: Optional[str] = Field(None, alias="PhoneAreaCode")
    phoneCountryCode: Optional[str] = Field(None, alias="PhoneCountryCode")


class XeroInvoiceItem(BaseModel):
    itemId: Optional[str] = Field(None, alias="ItemID")
    name: Optional[str] = Field(None, alias="Name")
    code: Optional[str] = Field(None, alias="Code")


class XeroInvoiceTracking(BaseModel):
    trackingCategoryId: Optional[str] = Field(None, alias="TrackingCategoryID")
    name: Optional[str] = Field(None, alias="Name")
    option: Optional[str] = Field(None, alias="Option")


class XeroInvoiceLineItem(BaseModel):
    itemCode: Optional[str] = Field(None, alias="ItemCode")
    description: Optional[str] = Field(None, alias="Description")
    quantity: Optional[str] = Field(None, alias="Quantity")
    unitAmount: Optional[str] = Field(None, alias="UnitAmount")
    taxType: Optional[str] = Field(None, alias="TaxType")
    taxAmount: Optional[str] = Field(None, alias="TaxAmount")
    lineAmount: Optional[str] = Field(None, alias="LineAmount")
    accountCode: Optional[str] = Field(None, alias="AccountCode")
    accountId: Optional[str] = Field(None, alias="AccountId")
    item: Optional[XeroInvoiceItem] = Field(None, alias="Item")
    tracking: Optional[List[XeroInvoiceTracking]] = Field(None, alias="Tracking")
    lineItemId: Optional[str] = Field(None, alias="LineItemID")


class XeroInvoicePayment(BaseModel):
    date: Optional[str] = Field(None, alias="Date")
    amount: Optional[str] = Field(None, alias="Amount") 
    paymentId: Optional[str] = Field(None, alias="PaymentID")


class XeroInvoice(BaseModel):
    """
    Represents an invoice in Xero.
    """

    model_config = ConfigDict(
        title="xeroInvoice",
        json_schema_mode_override="serialization",
        schema_generator=GlueSchemaGenerator(description="An invoice record from Xero containing details about the transaction, line items, customer information, payment status and financial amounts."),
    )

    invoiceId: str = Field(..., alias="InvoiceID")
    invoiceNumber: str = Field(..., alias="InvoiceNumber")
    type: Optional[str] = Field(None, alias="Type")
    contact: Optional[XeroInvoiceContact] = Field(None, alias="Contact")
    date: Optional[str] = Field(None, alias="Date")
    dateString: Optional[str] = Field(None, alias="DateString")
    dueDate: Optional[str] = Field(None, alias="DueDate")
    dueDateString: Optional[str] = Field(None, alias="DueDateString")
    status: Optional[str] = Field(None, alias="Status")
    lineAmountTypes: Optional[str] = Field(None, alias="LineAmountTypes")
    lineItems: Optional[List[XeroInvoiceLineItem]] = Field(None, alias="LineItems")
    subTotal: Optional[str] = Field(None, alias="SubTotal")
    totalTax: Optional[str] = Field(None, alias="TotalTax")
    total: Optional[str] = Field(None, alias="Total")
    updatedDateUTC: Optional[str] = Field(None, alias="UpdatedDateUTC")
    currencyCode: Optional[str] = Field(None, alias="CurrencyCode")
    payments: Optional[List[XeroInvoicePayment]] = Field(None, alias="Payments")
    amountDue: Optional[str] = Field(None, alias="AmountDue")
    amountPaid: Optional[str] = Field(None, alias="AmountPaid")
    amountCredited: Optional[str] = Field(None, alias="AmountCredited")
