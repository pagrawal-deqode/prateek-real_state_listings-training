from enum import Enum


class UserStatus(str, Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    DELETED = "DELETED"
    SUSPENDED = "SUSPENDED"


class ListingStatus(str, Enum):
    PENDING = "PENDING"
    PUBLISHED = "PUBLISHED"
    REJECTED = "REJECTED"
    WITHDRAWN = "WITHDRAWN"
    SUSPENDED = "SUSPENDED"
    UNDER_OFFER = "UNDER_OFFER"
    SOLD = "SOLD"
    RENTED = "RENTED"


class InquiryStatus(str, Enum):
    NEW = "NEW"
    CONTACTED = "CONTACTED"
    VISIT_SCHEDULED = "VISIT_SCHEDULED"
    CLOSED = "CLOSED"
    REJECTED = "REJECTED"


class ListingType(str, Enum):
    SALE = "SALE"
    RENT = "RENT"


class PropertyCategory(str, Enum):
    RESIDENTIAL = "RESIDENTIAL"
    COMMERCIAL = "COMMERCIAL"