# Vesture 🛒

**Vesture** is a Django-based e-commerce application that provides users with an intuitive shopping experience. The application includes user authentication, product listing, a shopping cart, a wishlist feature, and secure payment integration.

<!-- ## 🌍 Live Demo

You can access the live project here:  
**[Vesture Live](https://your-live-link.com)**  
 -->


## 🌟 Features

- **User Authentication**: Register, log in, log out, and manage user profiles.
- **Product Listings**: Browse products with detailed descriptions, images, and prices.
- **Shopping Cart**: Add items to the cart and update quantities before checkout.
- **Wishlist**: Save products to your wishlist for later viewing.
- **Payment Integration**: Secure payment processing for seamless transactions.

---

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS(Tailwind), JavaScript
- **Backend**: Django
- **Database**: SQLite (default, easily configurable to other databases)
- **Payment Gateway**: Integrated for secure transactions

---

## 🚀 Getting Started

Follow these steps to set up the project locally:

### Prerequisites

Ensure you have the following installed on your system:
- Python 3.9+ 
- Virtualenv (optional but recommended)
- Git

### Clone the Repository

```bash
git clone https://github.com/rebin03/Vesture.git
cd Vesture
```

### Set Up a Virtual Environment (Optional)

```bash
python -m venv venv
venv\Scripts\activate   # On Mac: source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Run the Development Server

```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser to view the application.


## 🛡️ Environment Variables

To ensure smooth functionality, set up the following environment variables:

### General

- `SECRET_KEY`: Your Django secret key
- `DEBUG`: Set to True for development, False for production
- `DATABASE_URL`: Database connection string (default is SQLite)
- `TWILIO_FROM_NUMBER`: Twilio phone number(Provided by twilio)
- `TO_NUMBER`: Destination phone number for testing

### Payment Gateway
Payment gateway credentials (if applicable)

### Mobile OTP Verification (Twilio)

- `TWILIO_RECOVERY_CODE`: Recovery code for Twilio
- `TWILIO_ACCOUNT_SID`: Twilio account SID
- `TWILIO_AUTH_TOKEN`: Twilio authentication token
- `ACCOUNT_SID`: Twilio account SID (alternate for OTP)
- `AUTH_TOKEN`: Twilio authentication token (alternate for OTP)
- `TWILIO_FROM_NUMBER`: Twilio phone number (provided by twilio)
- `TO_NUMBER`: Destination phone number for testing.

You can store these in a `.env` file for convenience.


## 📜 License
This project is licensed under the [MIT License](LICENSE).