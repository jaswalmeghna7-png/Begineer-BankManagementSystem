import streamlit as st
from bank import Bank

# Load backend data when the application starts
Bank.load_data()

# Page configuration
st.set_page_config(page_title="Bank Management System", layout="centered", page_icon="🏦")

st.title("🏦 Bank Management System")
st.markdown("Welcome! Choose an operation from the sidebar to manage your account.")

menu = ["Create Account", "Deposit Money", "Withdraw Money", "Show Details", "Update Details", "Delete Account"]
choice = st.sidebar.selectbox("Navigation Menu", menu)

# --- 1. CREATE ACCOUNT ---
if choice == "Create Account":
    st.subheader("📝 Open a New Account")
    with st.form("create_acc_form", clear_on_submit=True):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=1, max_value=120, step=1)
        email = st.text_input("Email Address")
        pin = st.number_input("Set 4-Digit Security PIN", min_value=1000, max_value=9999, step=1)
        submit = st.form_submit_button("Submit & Create Account")

    if submit:
        if not name or not email:
            st.warning("Please fill in all required text fields.")
        else:
            success, result = Bank.create_account(name, age, email, pin)
            if success:
                st.success("Account successfully created!")
                st.info(f"**Your Account Number:** `{result['accountNo']}` (Please save this!)")
                st.json(result)
            else:
                st.error(result)

# --- 2. DEPOSIT MONEY ---
elif choice == "Deposit Money":
    st.subheader("💵 Deposit Money")
    acc_no = st.text_input("Account Number")
    pin = st.number_input("4-Digit PIN", min_value=1000, max_value=9999, step=1, key="dep_pin")
    amount = st.number_input("Deposit Amount ($)", min_value=1, max_value=10000, step=10)
    
    if st.button("Deposit"):
        success, message = Bank.deposit_money(acc_no, pin, amount)
        if success:
            st.success(message)
        else:
            st.error(message)

# --- 3. WITHDRAW MONEY ---
elif choice == "Withdraw Money":
    st.subheader("💸 Withdraw Money")
    acc_no = st.text_input("Account Number")
    pin = st.number_input("4-Digit PIN", min_value=1000, max_value=9999, step=1, key="with_pin")
    amount = st.number_input("Withdrawal Amount ($)", min_value=1, step=10)
    
    if st.button("Withdraw"):
        success, message = Bank.withdraw_money(acc_no, pin, amount)
        if success:
            st.success(message)
        else:
            st.error(message)

# --- 4. SHOW DETAILS ---
elif choice == "Show Details":
    st.subheader("🔍 Account Profile & Balance")
    acc_no = st.text_input("Account Number")
    pin = st.number_input("4-Digit PIN", min_value=1000, max_value=9999, step=1, key="view_pin")
    
    if st.button("Fetch Details"):
        user = Bank.authenticate(acc_no, pin)
        if user:
            st.success(f"Welcome back, {user['name']}!")
            col1, col2 = st.columns(2)
            col1.metric("Current Balance", f"${user['Balance']}")
            col2.metric("Account Number", user['accountNo'])
            
            st.write("---")
            st.write(f"**Name:** {user['name']}")
            st.write(f"**Email:** {user['email']}")
            st.write(f"**Age:** {user['age']}")
        else:
            st.error("Invalid Account Number or PIN.")

# --- 5. UPDATE DETAILS ---
elif choice == "Update Details":
    st.subheader("⚙️ Update Account Information")
    acc_no = st.text_input("Account Number")
    pin = st.number_input("Current 4-Digit PIN", min_value=1000, max_value=9999, step=1, key="up_pin")
    
    st.markdown("---")
    st.caption("Leave blank any field you do not wish to update.")
    new_name = st.text_input("New Name")
    new_email = st.text_input("New Email")
    new_pin_input = st.text_input("New 4-Digit PIN (Optional)", type="password", max_chars=4)

    if st.button("Update Profile"):
        parsed_pin = None
        if new_pin_input:
            if new_pin_input.isdigit() and len(new_pin_input) == 4:
                parsed_pin = int(new_pin_input)
            else:
                st.error("New PIN must be a 4-digit number.")
                st.stop()

        success, message = Bank.update_details(acc_no, pin, new_name, new_email, parsed_pin)
        if success:
            st.success(message)
        else:
            st.error(message)

# --- 6. DELETE ACCOUNT ---
elif choice == "Delete Account":
    st.subheader("⚠️ Close Account")
    st.warning("Warning: This action is permanent and cannot be undone.")
    
    acc_no = st.text_input("Account Number")
    pin = st.number_input("4-Digit PIN", min_value=1000, max_value=9999, step=1, key="del_pin")
    confirm = st.checkbox("I understand that deleting my account will erase all profile data.")

    if st.button("Delete My Account"):
        if not confirm:
            st.error("Please check the confirmation box to proceed.")
        else:
            success, message = Bank.delete_account(acc_no, pin)
            if success:
                st.success(message)
            else:
                st.error(message)