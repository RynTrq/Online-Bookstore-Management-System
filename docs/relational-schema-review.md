# Relational Schema Review and Corrected Model

## Scope
This review is based on the original image `Screenshot 2024-06-22 162218.png` and the implemented SQL schemas (`Shoponize.sql` and `shoponize/schema.py`).

## Issues Found in the Screenshot

| Area | Problem in Screenshot | Correction Applied |
| --- | --- | --- |
| Naming consistency | Several typos and inconsistent labels (`Relational Schama`, `Adress`, mixed snake/camel, duplicate attributes) | Standardized names in SQL and SQLite schemas (for example `address_state`, `address_zipcode`, `address_street_name`) |
| Attributes | Incorrect/unclear attributes such as `Profile Pie`, `Adress_street_street Name`, and repeated street fields | Replaced with valid profile attributes and removed malformed duplicates |
| Domain constraints | No explicit domain rules shown for key business fields | Added checks for `gender` and `orderStatus` values |
| Relationship completeness | Logical relationships existed visually but local SQLite schema previously omitted some bridge tables | Added `contactNumber_customer`, `contactNumber_admin`, `contactNumber_supplier`, and `manages` to SQLite schema |
| Integrity visibility | Missing explicit cardinality behavior and delete semantics | Enforced referential actions via FK rules (`CASCADE`, `SET NULL`, `RESTRICT`) in physical schemas |

## Corrected Relational Model (Conceptual)

```mermaid
erDiagram
    CUSTOMER ||--|| CUSTOMER_PROFILE : has
    CUSTOMER ||--o{ CONTACT_NUMBER_CUSTOMER : has
    CUSTOMER ||--o{ ORDERS : places
    CUSTOMER ||--o{ CART : owns

    PRODUCT_CATEGORY ||--o{ PRODUCT : classifies
    PRODUCT ||--o{ CART : in_cart
    PRODUCT ||--o{ CONTAINS : ordered_as
    ORDERS ||--o{ CONTAINS : contains

    ADMIN ||--o{ CONTACT_NUMBER_ADMIN : has
    ADMIN ||--o{ MANAGES : manages
    PRODUCT_CATEGORY ||--o{ MANAGES : managed_by

    SUPPLIER ||--o{ CONTACT_NUMBER_SUPPLIER : has
    SUPPLIER ||--o{ SUPPLIES : supplies
    PRODUCT ||--o{ SUPPLIES : supplied_by

    CUSTOMER {
      int customerID PK
      string username UK
      string password
      char gender
      int loginAttempts
      bool isLocked
    }

    CUSTOMER_PROFILE {
      int customerID PK, FK
      string address_street_name
      string address_street_number
      string address_city
      string address_state
      string address_zipcode
      string payment
    }

    CONTACT_NUMBER_CUSTOMER {
      int customerID FK
      string number
    }

    ORDERS {
      int orderNumber PK
      int customerID FK
      date orderDate
      decimal amount
      string orderStatus
    }

    CONTAINS {
      int orderNumber FK
      int productID FK
      int quantity
      decimal unitPrice
    }

    PRODUCT_CATEGORY {
      int categoryID PK
      string name UK
      string description
    }

    PRODUCT {
      int productID PK
      string name
      decimal price
      int quantityAvailable
      bool isLowStock
      int categoryID FK
    }

    CART {
      int customerID FK
      int productID FK
      int quantity
    }

    ADMIN {
      int adminID PK
      string username UK
      string password
      int loginAttempts
      bool isLocked
    }

    CONTACT_NUMBER_ADMIN {
      int adminID FK
      string number
    }

    MANAGES {
      int adminID FK
      int categoryID FK
    }

    SUPPLIER {
      int supplierID PK
      string username UK
      string password
      int loginAttempts
      bool isLocked
    }

    CONTACT_NUMBER_SUPPLIER {
      int supplierID FK
      string number
    }

    SUPPLIES {
      int supplierID FK
      int productID FK
      int quantity
      decimal offerPrice
    }
```

## Physical Schema Alignment Result

The corrected model is now implemented in both:
- `Shoponize.sql` (MySQL)
- `shoponize/schema.py` (SQLite for local/dev tests)

This gives parity between local development and production-like relational behavior.
