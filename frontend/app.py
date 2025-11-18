import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_BASE = "http://127.0.0.1:8000"

st.title("📚 Bookstore Management Dashboard")

menu = st.sidebar.radio("Navigation", ["Inventory", "Sales", "Reports"])

# ---------------- Inventory Dashboard ----------------
if menu == "Inventory":
    st.header("Manage Inventory")

    # Add Book
    st.subheader("Add New Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    category = st.text_input("Category")
    price = st.number_input("Price", min_value=0.0)
    stock = st.number_input("Stock", min_value=0)
    isbn = st.text_input("ISBN")

    if st.button("Add Book"):
        payload = {"title": title, "author": author, "category": category, "price": price, "stock": stock, "isbn": isbn}
        res = requests.post(f"{API_BASE}/books/", params=payload)
        if res.status_code == 200:
            st.success("Book added successfully!")
        else:
            st.error("Failed to add book")

    # View Books
    st.subheader("Current Inventory")
    books = requests.get(f"{API_BASE}/books/").json()
    if books:
        df_books = pd.DataFrame(books)
        st.dataframe(df_books)

        # Update Stock
        st.subheader("Update Stock")
        book_id = st.selectbox("Select Book ID", df_books['id'])
        new_stock = st.number_input("New Stock", min_value=0)
        if st.button("Update Stock"):
            res = requests.put(f"{API_BASE}/books/{book_id}", params={"stock": new_stock})
            if res.status_code == 200:
                st.success("Stock updated successfully!")
            else:
                st.error("Failed to update stock")

        # Delete Book
        st.subheader("Delete Book")
        del_book_id = st.selectbox("Select Book to Delete", df_books['id'])
        if st.button("Delete Book"):
            res = requests.delete(f"{API_BASE}/books/{del_book_id}")
            if res.status_code == 200:
                st.success("Book deleted successfully!")
            else:
                st.error("Failed to delete book")

# ---------------- Sales Form ----------------
elif menu == "Sales":
    st.header("Record a Sale")
    books = requests.get(f"{API_BASE}/books/").json()
    customers = requests.get(f"{API_BASE}/customers/").json()

    if books and customers:
        book_id = st.selectbox("Select Book", [b['id'] for b in books])
        customer_id = st.selectbox("Select Customer", [c['id'] for c in customers])
        quantity = st.number_input("Quantity", min_value=1)

        if st.button("Record Sale"):
            payload = {"book_id": book_id, "customer_id": customer_id, "quantity": quantity}
            res = requests.post(f"{API_BASE}/sales/", params=payload)
            if res.status_code == 200:
                st.success("Sale recorded successfully!")
            else:
                st.error("Failed to record sale")
    else:
        st.warning("Please add books and customers first.")

# ---------------- Reports ----------------
elif menu == "Reports":
    st.header("Sales Reports")
    sales = requests.get(f"{API_BASE}/sales/").json()
    if sales:
        df_sales = pd.DataFrame(sales)
        st.subheader("Sales Data")
        st.dataframe(df_sales)

        # Top Selling Books
        st.subheader("Top Selling Books")
        top_books = df_sales.groupby('book_id')['quantity'].sum().reset_index()
        fig_books = px.bar(top_books, x='book_id', y='quantity', title='Top Selling Books')
        st.plotly_chart(fig_books)

        # Revenue Trend
        st.subheader("Revenue Trend")
        df_sales['sale_date'] = pd.to_datetime(df_sales['sale_date'])
        revenue_trend = df_sales.groupby(df_sales['sale_date'].dt.date)['total_price'].sum().reset_index()
        fig_revenue = px.line(revenue_trend, x='sale_date', y='total_price', title='Revenue Over Time')
        st.plotly_chart(fig_revenue)
    else:
        st.warning("No sales data available.")