import streamlit as st
from food_delivery import Customer, Restaurant, MenuItem, DeliveryPartner

st.set_page_config(page_title="Food Delivery System", page_icon="🍔")

# Session state
if "customer" not in st.session_state:
    st.session_state.customer = None

if "restaurant" not in st.session_state:
    restaurant = Restaurant("Bawarchi", "MG Road")
    restaurant.add_item(MenuItem("Biryani", 250, False))
    restaurant.add_item(MenuItem("Kebab", 180, False))
    restaurant.add_item(MenuItem("Paneer Tikka", 200, True))
    restaurant.add_item(MenuItem("Veg Biryani", 180, True))
    st.session_state.restaurant = restaurant

if "partner" not in st.session_state:
    st.session_state.partner = None

if "order" not in st.session_state:
    st.session_state.order = None

st.title("🍔 Food Delivery System")
st.write("Simple Streamlit interface for the OOP Food Delivery project.")

# ---------------- CUSTOMER ----------------
st.header("1. Create Customer")

with st.form("customer_form"):
    name = st.text_input("Customer Name")
    phone = st.text_input("Phone Number")
    address = st.text_input("Address")
    create_customer = st.form_submit_button("Create Customer")

if create_customer:
    if name and phone and address:
        st.session_state.customer = Customer(name, phone, address)
        st.success(f"Customer {name} created successfully!")
    else:
        st.warning("Please fill all customer details.")

if st.session_state.customer:
    customer = st.session_state.customer
    st.info(
        f"Customer: {customer._name} | "
        f"Wallet: ₹{customer._wallet_balance:.2f}"
    )

# ---------------- WALLET ----------------
st.header("2. Add Wallet Balance")

if st.session_state.customer:
    with st.form("wallet_form"):
        amount = st.number_input(
            "Amount",
            min_value=0.0,
            step=50.0
        )
        add_money = st.form_submit_button("Add Money")

    if add_money:
        st.session_state.customer.add_to_wallet(amount)
        st.success(f"₹{amount:.2f} added to wallet.")

    st.write(
        f"**Current Wallet Balance:** "
        f"₹{st.session_state.customer._wallet_balance:.2f}"
    )
else:
    st.warning("Create a customer first.")

# ---------------- RESTAURANT MENU ----------------
st.header("3. Restaurant Menu")

restaurant = st.session_state.restaurant
st.subheader(f"{restaurant.name} - {restaurant.location}")

menu = restaurant.get_menu()

for i, item in enumerate(menu):
    veg = "🟢 Veg" if item.is_veg else "🔴 Non-Veg"
    st.write(f"**{i + 1}. {item.name}** — ₹{item.price} — {veg}")

# ---------------- PLACE ORDER ----------------
st.header("4. Place Order")

if st.session_state.customer:
    selected_items = st.multiselect(
        "Select food items",
        options=menu,
        format_func=lambda item: f"{item.name} - ₹{item.price}"
    )

    if st.button("Place Order"):
        if not selected_items:
            st.warning("Please select at least one item.")
        else:
            customer = st.session_state.customer
            order = customer.place_order(restaurant, selected_items)
            st.session_state.order = order

            st.success(f"Order {order._order_id} placed successfully!")
            st.info("OTP for delivery: 1234")

else:
    st.warning("Create a customer before placing an order.")

# ---------------- ORDER DETAILS ----------------
if st.session_state.order:
    order = st.session_state.order

    st.header("5. Order Details")

    subtotal = order.subtotal()
    gst = subtotal * 0.05
    packaging = 20
    total = order.calculate_bill()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Order ID", order._order_id)
    col2.metric("Subtotal", f"₹{subtotal:.2f}")
    col3.metric("GST", f"₹{gst:.2f}")
    col4.metric("Total", f"₹{total:.2f}")

    st.write(f"**Packaging Fee:** ₹{packaging}")
    st.write(f"**Estimated Time:** {order.estimated_time()} minutes")
    st.write(f"**Order Status:** `{order._status}`")

# ---------------- DELIVERY PARTNER ----------------
st.header("6. Create Delivery Partner")

with st.form("partner_form"):
    partner_name = st.text_input("Partner Name")
    partner_phone = st.text_input("Partner Phone")
    vehicle = st.selectbox("Vehicle", ["Bike", "Scooter", "Car"])
    create_partner = st.form_submit_button("Create Delivery Partner")

if create_partner:
    if partner_name and partner_phone:
        st.session_state.partner = DeliveryPartner(
            partner_name,
            partner_phone,
            vehicle
        )
        st.success(f"Delivery partner {partner_name} created!")
    else:
        st.warning("Please fill partner name and phone.")

# ---------------- ACCEPT ORDER ----------------
st.header("7. Accept Order")

if st.session_state.partner and st.session_state.order:
    partner = st.session_state.partner
    order = st.session_state.order

    st.write(f"Partner available: **{partner.is_available}**")
    st.write(f"Order status: **{order._status}**")

    if st.button("Accept Order"):
        if order._status != "Placed":
            st.warning("This order cannot be accepted.")
        elif partner.accept_order(order):
            st.success("Order accepted by delivery partner!")
            st.rerun()
        else:
            st.error("Delivery partner is not available.")
else:
    st.info("Create a delivery partner and place an order first.")

# ---------------- OTP DELIVERY ----------------
st.header("8. Complete Delivery")

if st.session_state.partner and st.session_state.order:
    partner = st.session_state.partner
    order = st.session_state.order

    otp = st.text_input("Enter Customer OTP", type="password")

    if st.button("Verify OTP & Complete Delivery"):
        if order._status != "Accepted":
            st.warning("Order must be Accepted before delivery.")
        elif not otp:
            st.warning("Please enter the OTP.")
        elif partner.deliver(order, otp):
            if st.session_state.customer:
                st.session_state.customer.notify("Order delivered successfully!")
            partner.notify("Order delivered successfully!")

            st.success("✅ Delivery completed successfully!")
            st.balloons()
            st.rerun()
        else:
            st.error("❌ Wrong OTP. Delivery not completed.")

# ---------------- CURRENT STATUS ----------------
st.header("9. Current Status")

if st.session_state.order:
    order = st.session_state.order
    st.write(f"**Order:** {order._order_id}")
    st.write(f"**Status:** {order._status}")

if st.session_state.partner:
    st.write(
        f"**Delivery Partner Available:** "
        f"{st.session_state.partner.is_available}"
    )
