# AppetiEats
#### Video Demo: <URL>
#### Description: ApppetiEats is an Online Delivery Web Application that simplifies the gastronomic experience by allowing restaurants to display their menus and allowing their customers to place orders in an easy and intuitive way.
### This is my CS50 final project

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [Structure](#structure)
- [License](#license)

## Instalation

To set up AppetiEats, follow these steps:

```bash
# Clone the repository
git clone https://github.com/valentejorge/appetieats/

# Navigate to the project directory
cd AppetiEats

# Install required dependencies
pip install -r requirements.txt

# Load sample data
flask restart-db
```

## Usage

1. Start the application: 

```bash
flask run
```

2. Access the aplication through your web browser at `http://localhost:5000`

3. Restaurants can sign up, log in, add their menu items, generate a restaurant QR Code, and see orders in real-time in restaurant dashboard.

4. Customers can access restaurants menu through the QR code or a link, view menu, place orders, and track status of orders in real-time.

## Features

- **Restaurant Registration**: Restaurants can sign up and create accounts to showcase their menus.
- **Menu Management**: Restaurants can add, edit, or remove items from their menus through an intuitive dashboard.
- **Customer Orders**: Customers can access a restaurant menus, place orders, and track their order status in real-time.
- **User Authentication**: Secure user authentication for both restaurants and customers.
- **Order History**: Customers and restaurants can view their order history.

## Project Structure

```bash
.
├── appetieats (MAIN PACKAGE)
│   ├── app.py (APP FACTORIES)
│   ├── models.py (DATABASE MODELS)
│   ├── requirements.py (APP REQUIREMENTS)
│   ├── __init__.py
│   ├── ext (EXTENSIONS FACTORIES)
│   │   ├── __init__.py
│   │   ├── commands.py
│   │   ├── configuration.py
│   │   ├── database.py
│   │   ├── error.py
│   │   ├── events.py
│   │   ├── sesssion.py
│   │   └── helpers (HELPERS FUNCTIONS)
│   │       ├── __init__.py
│   │       ├── cache_images.py
│   │       ├── db_tools.py
│   │       ├── get_inputs.py
│   │       ├── register_tools.py
│   │       ├── sample_data.json
│   │       └── validate_inputs.py
│   │       
│   ├── routes (APP ROUTES)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── customer.py
│   │   ├── main.py
│   │   ├── menu.py
│   │   ├── admin
│   │   │   ├── admin.py
│   │   │   └── settings.py
│   ├── static (STATIC FILES)
│   │   ├── assets
│   │   │   └── ...
│   │   ├── cache 
│   │   ├── css (CSS FILES)
│   │   │   └── ...
│   │   ├── js (JAVASCRIPT FILES)
│   │   │   ├── ...
│   │   │   ├── admin
│   │   │   │   ├── ...
│   │   │   │   └── socketio.js (WEBHOOKS SETTINGS)
│   │   │   ├── customer
│   │   │   │   ├── ...
│   │   │   │   └── socketio.js (WEBHOOKS SETTINGS)
│   │   │   ├── menu
│   │   │   │   ├── cart.js (CART SETTINGS)
│   │   │   │   └── ...
│   │   │   └── ...
│   │   └── sample_data (SAMPLE DATA FOR POPULATE DB)
│   │       ├── bacon.png
│   │       ├── ...
│   │       └── ...
│   └── templates (APP TEMPLATES)
│       ├── admin
│       │   ├── dashboard.html (RESTAURANT DASHBOARD)
│       │   ├── settings
│       │   │   ├── ...
│       │   │   └── qr-code.html (QR CODE GENERATOR)
│       │   └── settings.html
│       ├── auth
│       │   └── ...
│       ├── customer
│       │   └── ...
│       ├── ...
│       └── menu
│           └── ...
├── instance (FLASK INSTANCE)
│   └── database.db
├── LICENSE
├── settings.toml (APP SETTINGS)
└── README.md
```

## License 

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License
```
