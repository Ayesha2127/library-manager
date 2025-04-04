import streamlit as st
import json

# Custom CSS (only for title/subheader sizing and background)
st.markdown("""
<style>
    .big-title {
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0 !important;
        color: #6e48aa;
    }
    .small-subheader {
        font-size: 1.1rem !important;
        color: #7f7f7f !important;
        margin-top: 0 !important;
    }
    .stApp {
        background-color: #f9f9f9 !important;
    }
    .sidebar .sidebar-content {
        background-color: #2d3436 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- YOUR ORIGINAL CODE WITH ENGLISH SUCCESS MESSAGES ---
def load_library():
    try:
        with open("library.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_library():
    with open("library.json", "w") as file:
        json.dump(library, file)

library = load_library()

st.markdown('<p class="big-title">Libro</p>', unsafe_allow_html=True)
st.markdown('<p class="small-subheader">Personal Library Manager</p>', unsafe_allow_html=True)

# Sidebar menu
menu = st.sidebar.radio(
    "Select an option",
    ["Add Book", "View Library", "Remove Book", "Search Book", "Save and Exit"],
)

# View Library
if menu == "View Library":
    st.sidebar.subheader("Your Library")
    if library:
        st.table(library)
    else:
        st.write("Library is empty.")

# Add Book
elif menu == "Add Book":
    st.sidebar.subheader("Add a new Book")
    title = st.text_input("Title")
    author = st.text_input("Author")
    year = st.number_input("Year", min_value=0, step=1)
    genre = st.text_input("Genre")
    read_status = st.checkbox("Already Read")

    if st.button("Add Book"):
        library.append(
            {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read_status": read_status,
            }
        )
        save_library()
        st.success(f"Book '{title}' added successfully!") 
        st.rerun()

# Remove Book
elif menu == "Remove Book":
    st.sidebar.subheader("Remove a Book")
    if library:
        book_titles = [book["title"] for book in library]
        if book_titles:
            selected_book = st.selectbox("Select a book to remove", book_titles)
            if st.button("Remove Book"):
                library = [book for book in library if book["title"] != selected_book]
                save_library()
                st.success(f"Book '{selected_book}' removed successfully!") 
                st.rerun()
        else:
            st.write("No books available to remove. Add books first.")

# Search Book
elif menu == "Search Book":
    st.sidebar.subheader("Search a Book")
    if library:
        search_term = st.text_input("Enter title or author to search")
        if st.button("Search"):
            results = [
                book
                for book in library
                if search_term.lower() in book["title"].lower()
                or search_term.lower() in book["author"].lower()
            ]
            if results:
                st.table(results)
            else:
                st.write("No matching books found.")
    else:
        st.write("Library is empty.")

# Save and Exit
elif menu == "Save and Exit":
    st.sidebar.subheader("Save and Exit")
    save_library()
    st.success("Library saved successfully!")