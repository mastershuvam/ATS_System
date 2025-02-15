import stripe
import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Set up Stripe API key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Streamlit UI
st.title("💳 Secure Payment for Resume Analysis")

# Pricing details
price_options = {
    "Basic Evaluation": 5000,   # $50.00 (Stripe works in cents)
    "Advanced Analysis": 10000, # $100.00
    "Full ATS Optimization": 15000 # $150.00
}

# User selects a service
selected_service = st.selectbox("Choose a Service", list(price_options.keys()))

# Button to initiate payment
if st.button("Proceed to Payment 💰"):
    try:
        # Create a Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': selected_service,
                    },
                    'unit_amount': price_options[selected_service],  # Amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url="https://yourdomain.com/success",  # Replace with actual success page
            cancel_url="https://yourdomain.com/cancel",   # Replace with actual cancel page
        )

        # Redirect user to Stripe Checkout page
        st.write("✅ Click the button below to complete your payment:")
        st.markdown(f"[Pay Now]({session.url})", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"❌ Payment failed: {str(e)}")
