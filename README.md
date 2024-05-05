# Vendor Management System with Performance Metrics

## Overview

This project implements a Vendor Management System using Django and Django REST Framework. The system includes features for managing vendor profiles, tracking purchase orders, and calculating vendor performance metrics.

## Features

- **Vendor Profile Management:**
  - Create, retrieve, update, and delete vendor profiles.
- **Purchase Order Tracking:**
  - Create, retrieve, update, and delete purchase orders.
- **Vendor Performance Evaluation:**
  - Calculate and retrieve vendor performance metrics.
- **Purchase Order Acknowledgement:**
  - can update acknowledgment time.
 
  ### Prerequisites

- Python 3.6+
- Django
- Django RestFrameWork  
- Pip
1. Clone the repository:

    ```bash
    git clone [https://github.com/yourusername/vendor-management-system.git](https://github.com/dkd99/vendor-management-system.git)
    cd vendor-management-system
    ```

2. Set up a virtual environment (optional but recommended):
    python -m venv venv
    source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'

3. Install dependencies:

    pip install -r requirements.txt

4. Apply migrations:

    ```bash
    python manage.py migrate
    ```

5. Run the development server:

    ```bash
    python manage.py runserver
    ```

The API should now be accessible at `http://127.0.0.1:8000/`.

## API Endpoints
-**Rigistration Endpoints:**
   - POST 'account/register/ : creates a user with username as vendor code and also craetes a vendor object.
   - POST 'account/login/: creates a token for vendor who is trying to login.
   - POST 'account/logout/ : destroys the authtoken, hence logging out the vendor.
- **Vendor Endpoints:**
  - POST `/api/vendors/`: Create a new vendor. --could have been created with this but the vendor can be created by registering the vendor. Only admin user is permitted for this request.
  - GET `/api/vendors/`: List all vendors.
  - GET `/api/vendors/{id}/`: Retrieve a specific vendor's details.
  - PUT `/api/vendors/{id}/`: Update a vendor's details. -- only the specific vendor and admin allowed to update only name, contact details and address. Other fields are updated throgh signals
                              when certain fields are edited in purchase order by vendor.
  - DELETE `/api/vendors/{id}/`: Delete a vendor.-- only the specific vendor and admin allowed to delete.

- **Purchase Order Endpoints:**
  - POST `/api/purchase_orders/`: Create a purchase order. -- can be created by admin.
  - GET `/api/purchase_orders/`: List all purchase orders with an option to filter by vendor. 
  - GET `/api/purchase_orders/{po_id}/`: Retrieve details of a specific purchase order. 
  - PUT `/api/purchase_orders/{po_id}/`: Update a purchase order. -- only the vendor to whom purchase order is assigned can edit and update fields.
  - DELETE `/api/purchase_orders/{po_id}/`: Delete a purchase order.

- **Vendor Performance Endpoint:**
  - GET `/api/vendors/{id}/performance`: Retrieve a vendor's performance metrics.

- **Update Acknowledgment Endpoint:**
  - POST `/api/purchase_orders/{po_id}/acknowledge`: Acknowledge a purchase order. --only admin and vendor to which the purchase order is assigned is allowed to update this field.

## Backend Logic for Performance Metrics

- **On-Time Delivery Rate:**
  - Calculated each time a PO status changes to 'completed'.
  - Logic: Count the number of completed POs delivered on or before delivery_date and divide by the total number of completed POs for that vendor. When a purchase order is created a expected delivery date is 
           assigned and status is pending. When order is marked completed, a signal is generated throgh which actual delivery and expected delivery  are compared.  On-Time Delivery Rate is updated.

- **Quality Rating Average:**
  - Updated upon the completion of each PO where a quality_rating is provided.
  - Logic: Calculate the average of all quality_rating values for completed POs of the vendor. Whenever a order status is marked as completed and a quality rating is provided,  Quality Rating Average is calculated 
           through django signal.

- **Average Response Time:**
  - Calculated each time a PO is acknowledged by the vendor.
  - Logic: Compute the time difference between issue_date and acknowledgment_date for each PO, and then find the average of these times for all POs of the vendor. Whenever, acknowledgement date is updated by 
           the vendor to whom the purchase order is assigned , a signal is used to calculate Average Response Time.

- **Fulfillment Rate:**
  - Calculated upon any change in PO status.
  - Logic: Divide the number of successfully fulfilled POs (status 'completed' without issues) by the total number of POs issued to the vendor. 
- **Trend Analysis:**
    The function update_historical_performance is a signal receiver that listens for changes in a vendor model.It checks if the vendor instance already exists (if instance.pk).
    If it does, it proceeds with further actions. It retrieves the last historical performance record for the vendor (last_record) using filter() and latest() methods.It calculates the
    time difference between the current time and the date of the last historical performance record.It checks if a week has passed since the last update by comparing the time difference
    with a timedelta of one week.If a week(can be adjusted as per requirement) has passed, it creates a new historical performance record (HistoricalPerformance.objects.create()) with the updated metrics from the vendor instance.
    Trend analysis can be performed through the historical records of particular vendor.

## Technical Requirements

- **Django Version:** 3.2 (latest stable)
- **Django REST Framework Version:** 3.12 (latest stable)
- **Database:** SQLite (default in Django)
- **Authentication:** Token-based authentication. Custom permissions have been used for all views based on requirements.
- **Coding Style:** PEP 8

To run the test suite, use the following command:


 python manage.py test 
