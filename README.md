# Vibing Clothe E-commerce Project

This is a Django-based e-commerce project named "Vibing Clothe", implementing various features including product management, a shopping cart, user authentication, order processing with Stripe integration, product reviews, wishlists, and discount coupons.

## Table of Contents

-   [Features](#features)
-   [Installation](#installation)
-   [Running the Project](#running-the-project)
-   [Project Structure](#project-structure)
-   [Test Data Generation](#test-data-generation)
-   [Design Decisions](#design-decisions)
-   [Testing](#testing)
-   [Optional Features Implemented](#optional-features-implemented)
-   [State Diagrams](#state-diagrams)

## Features

**Functional Requirements Implemented:**
1.  **Product Management:** List products with image, name, description, and price; filter by category; search by name/description; view product details.
2.  **Shopping Cart:** Add/modify/remove products (with quantity); view cart with subtotals and total; empty cart; persist cart data (session-based).
3.  **User Management:** User registration, login/logout, user profile with personal data, and order history.
4.  **Checkout Process:** Shipping data form, simulated payment (Stripe integration), order confirmation with order number.

**Non-Functional Requirements Implemented:**
1.  **User Interface:** Responsive design using Bootstrap, with custom CSS for a modern look ("Vibing Clothe" theme).
2.  **Validation:** Form data validation (server-side, with client-side provided by Django/Bootstrap).
3.  **Security:** Authentication-required routes protected.
4.  **Messaging:** Django's messages framework can be integrated for success/error/warning messages (though not explicitly shown in all current views).
5.  **Code Quality:** Good practices applied, clean and commented code where necessary.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd Proyecto Django
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    "C:\Program Files\Python314-arm64\python.exe" -m venv .venv
    .venv\Scripts\activate
    ```
    *Note: If `activate` script fails due to execution policy, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` in PowerShell.*

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    # Follow prompts to create username, email, and password
    ```
    *Alternatively, you can create a superuser with pre-defined credentials for quick setup:*
    ```bash
    python manage.py createsuperuser --noinput --username admin --email admin@example.com
    python manage.py changepassword admin # Set password to 'admin'
    ```

## Running the Project

1.  **Activate your virtual environment (if not already active):**
    ```bash
    .venv\Scripts\activate
    ```

2.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

3.  **Access the application:**
    Open your web browser and go to `http://127.0.0.1:8000/`.

4.  **Access the admin panel:**
    Open your web browser and go to `http://127.0.0.1:8000/admin/`. Log in with your superuser credentials.

## Project Structure

```
.
├── cart/                   # Shopping cart application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── cart.py             # Core cart logic (add, remove, total)
│   ├── forms.py            # Forms related to cart (e.g., add product quantity)
│   ├── migrations/
│   ├── models.py
│   ├── templates/
│   │   └── cart/
│   │       └── detail.html # Cart detail page
│   ├── urls.py
│   └── views.py            # Cart views (add, remove, detail)
├── ecommerce/              # Main Django project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py         # Project settings (database, installed apps, etc.)
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py
├── orders/                 # Order processing application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py            # Order creation form, coupon apply form
│   ├── migrations/
│   ├── models.py           # Order, OrderItem, Coupon models
│   ├── templates/
│   │   ├── admin/
│   │   │   └── dashboard.html # Admin dashboard for statistics
│   │   └── orders/
│   │       └── order/
│   │           ├── canceled.html # Payment canceled page
│   │           ├── create.html   # Order creation form
│   │           └── created.html  # Order confirmation page
│   ├── urls.py
│   └── views.py            # Order creation, payment (Stripe), admin dashboard, PDF export
├── store/                  # Product catalog application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py # Makes categories available globally
│   ├── forms.py            # Review form
│   ├── migrations/
│   ├── models.py           # Category, Product, Review models
│   ├── static/
│   │   └── img/
│   │       └── no_image.png # Placeholder image
│   ├── templates/
│   │   └── store/
│   │       ├── base.html       # Base template for the store (header, footer, navbar)
│   │       └── product/
│   │           ├── detail.html # Product detail page
│   │           └── list.html   # Product list page (landing page)
│   ├── urls.py
│   └── views.py            # Product list, product detail
├── users/                  # User authentication and profile application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py            # User registration form
│   ├── migrations/
│   ├── models.py           # Wishlist model
│   ├── templates/
│   │   └── users/
│   │       ├── login.html      # Login page
│   │       ├── logged_out.html # Logout confirmation page
│   │       ├── profile.html    # User profile and order history
│   │       └── register.html   # User registration page
│   ├── urls.py
│   └── views.py            # User registration, profile, wishlist management
├── manage.py               # Django's command-line utility
└── requirements.txt        # Python dependencies
```

## Test Data Generation

To populate your database with sample products and categories, run the following management command:

```bash
python manage.py create_sample_data
```
*Note: This command will create 50 sample products and several categories. It will also create a dummy coupon.*

## Design Decisions

-   **Modular Application Structure:** The project is organized into modular Django apps (`store`, `cart`, `users`, `orders`) to promote separation of concerns, reusability, and maintainability.
-   **Session-based Cart:** The shopping cart uses Django sessions for persistence, providing a seamless experience for anonymous and authenticated users alike.
-   **Stripe Integration:** For payment processing, Stripe Checkout is integrated in test mode, offering a secure and widely adopted solution for e-commerce transactions. This keeps sensitive payment information off the store's servers.
-   **User-Friendly Authentication:** Django's built-in authentication system is leveraged for user management, with custom forms for registration and automatic login post-registration to enhance user experience. Password requirements are relaxed for development/demonstration purposes but can be easily re-enabled.
-   **Responsive UI with Bootstrap:** Bootstrap 5 is used for a responsive and modern user interface, ensuring the store looks good on various devices. Custom CSS further refines the aesthetic to the "Vibing Clothe" theme.
-   **Global Context Processors:** Categories and cart information are made globally available to all templates via context processors, reducing redundant data fetching in views.
-   **Data Population via Migrations/Commands:** Initial product data and categories are populated through Django migrations and a custom management command, making the setup repeatable and version-controlled.
-   **Placeholder Images:** Placeholder image URLs are used to provide visual representation for products without requiring actual image uploads during development.
-   **Clear URL Structure:** URLs are organized using app namespaces for clarity and to prevent conflicts.

## Testing

To run the unit tests, use the following command:

```bash
python manage.py test
```

### Test Cases

The project includes unit tests for the core functionalities across the `store`, `cart`, `users`, and `orders` applications.

#### `store` App Tests (7 tests)
-   **`test_category_creation`**: Verifies that a `Category` object can be created correctly, including its `name`, `slug`, string representation, and absolute URL.
-   **`test_product_creation`**: Ensures that a `Product` object can be created with all its attributes (`name`, `slug`, `price`, `availability`), and checks its string representation and absolute URL.
-   **`test_review_creation`**: Confirms that a `Review` object can be successfully created, linked to a `Product` and `User`, and that the `Product`'s average `rating` is updated automatically upon review creation.
-   **`test_product_rating_update`**: Validates that the `Product`'s `rating` is correctly recalculated and updated when new reviews are added.
-   **`test_product_rating_delete_review`**: Checks that the `Product`'s `rating` is accurately adjusted when a review is deleted.

#### `cart` App Tests (7 tests)
-   **`test_cart_add`**: Tests adding a single product to the cart and verifies the cart's length and total price.
-   **`test_cart_add_multiple_items`**: Verifies the cart's behavior when multiple items (different products or multiple quantities of the same product) are added.
-   **`test_cart_add_override_quantity`**: Ensures that overriding the quantity of an existing product in the cart works as expected.
-   **`test_cart_remove`**: Confirms that products can be successfully removed from the cart.
-   **`test_cart_clear`**: Verifies that the entire cart can be cleared, resetting its contents and total.
-   **`test_cart_iter`**: Checks the iteration mechanism of the `Cart` class, ensuring that all items are correctly represented as dictionaries with associated product objects.
-   **`test_cart_get_total_price_after_discount_no_coupon`**: Verifies the total price calculation when no coupon is applied.
-   **`test_cart_get_total_price_after_discount_with_coupon`**: Confirms that the total price correctly reflects the discount when a valid coupon is applied.

#### `users` App Tests (7 tests)
-   **`test_registration`**: Tests the user registration process, ensuring a new user is created and redirected after successful registration.
-   **`test_login`**: Verifies the user login functionality, ensuring successful authentication and session management.
-   **`test_logout`**: Confirms that a user can successfully log out, clearing their session.
-   **`test_profile_view`**: Checks that an authenticated user can access their profile page and that the correct template is used.
-   **`test_wishlist_add`**: Verifies that a product can be added to a user's wishlist.
-   **`test_wishlist_remove`**: Ensures that a product can be successfully removed from a user's wishlist.
-   **`test_wishlist_view`**: Tests the wishlist display, ensuring it shows the correct items for the authenticated user.

#### `orders` App Tests (7 tests)
-   **`test_order_creation_no_coupon`**: Verifies the creation of an order without a discount coupon, checking the order details and total cost.
-   **`test_order_creation_with_coupon`**: Ensures that an order is created correctly when a valid coupon is applied, checking the discount and final total cost.
-   **`test_payment_completed`**: Tests the `payment_completed` view, confirming that the order's `paid` status is updated and the user is redirected to the confirmation page.
-   **`test_payment_canceled`**: Verifies the behavior of the `payment_canceled` view, ensuring the correct template is rendered.
-   **`test_admin_dashboard_access`**: Checks access control for the admin dashboard, ensuring only staff members can view it.
-   **`test_admin_dashboard_data`**: Validates that the admin dashboard correctly displays statistics such as total products, orders, and revenue.
-   **`test_admin_order_pdf_access`**: Tests access control for the PDF order export function and verifies that a PDF is generated for staff members.


## Optional Features Implemented

The following optional features have been implemented:

-   **Product Ratings and Reviews:** Users can submit ratings and text reviews for products. The product's average rating is automatically updated.
-   **Integrate API of payments (Stripe in test mode):** Stripe Checkout is used for a secure and integrated payment flow.
-   **Add wishlist (lista de deseos):** Authenticated users can add and remove products from a personal wishlist.
-   **Sistema de cupones de descuento:** Discount coupons can be created and applied in the cart, affecting the total order price.
-   **Custom admin panel with statistics:** A basic admin dashboard is available, displaying key statistics like total products, orders, and revenue.
-   **Export orders to PDF:** Staff users can export individual order details to a PDF invoice directly from the admin.

## State Diagrams

*To be implemented in the next steps.*
