import json
import streamlit as st

class LibraryManager:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.library = self.load_library()

    def load_library(self):
        """📂 Load the library from a file."""
        try:
            with open(self.filename, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_library(self):
        """💾 Save the library to a file."""
        with open(self.filename, "w") as file:
            json.dump(self.library, file, indent=4)

    def add_book(self, title, author, year, genre, read_status):
        """📖 Add a book to the library."""
        self.library.append({
            "title": title,
            "author": author,
            "year": year,
            "genre": genre,
            "read_status": read_status
        })
        self.save_library()

    def remove_book(self, title):
        """🗑 Remove a book by title."""
        self.library = [book for book in self.library if book["title"].lower() != title.lower()]
        self.save_library()

    def search_book(self, query):
        """🔍 Search for a book by title or author."""
        return [book for book in self.library if query.lower() in book["title"].lower() or query.lower() in book["author"].lower()]

    def display_books(self):
        """📚 Return all books in the library."""
        return sorted(self.library, key=lambda x: x["title"].lower())

    def display_statistics(self):
        """📊 Display statistics about the library."""
        total_books = len(self.library)
        read_books = sum(1 for book in self.library if book["read_status"])
        read_percentage = (read_books / total_books * 100) if total_books else 0
        return total_books, read_books, read_percentage

manager = LibraryManager()

st.title("📚 Personal Library Manager")

menu = st.sidebar.selectbox("Menu", ["Add a Book", "Remove a Book", "Search for a Book", "Display All Books", "Statistics"])

if menu == "Add a Book":
    st.header("📖 Add a New Book")
    title = st.text_input("📕 Title")
    author = st.text_input("✍️ Author")
    year = st.number_input("📅 Year", min_value=0, max_value=9999, step=1)
    genre = st.text_input("📚 Genre")
    read_status = st.checkbox("✅ Read")
    if st.button("Add Book"):
        manager.add_book(title, author, year, genre, read_status)
        st.success("📗 Book added successfully!")

elif menu == "Remove a Book":
    st.header("🗑 Remove a Book")
    title = st.text_input("❌ Enter the title to remove")
    if st.button("Remove Book"):
        manager.remove_book(title)
        st.success("🗑 Book removed successfully!")

elif menu == "Search for a Book":
    st.header("🔍 Search for a Book")
    query = st.text_input("🔎 Enter title or author")
    if st.button("Search"):
        results = manager.search_book(query)
        if results:
            for book in results:
                st.write(f"📖 {book['title']} - ✍️ {book['author']} - 📅 {book['year']} - 📚 {book['genre']} - ✅ {'Read' if book['read_status'] else 'Unread'}")
        else:
            st.warning("⚠️ No matching books found.")

elif menu == "Display All Books":
    st.header("📚 All Books")
    books = manager.display_books()
    if books:
        for book in books:
            st.write(f"📖 {book['title']} - ✍️ {book['author']} - 📅 {book['year']} - 📚 {book['genre']} - ✅ {'Read' if book['read_status'] else 'Unread'}")
    else:
        st.warning("📭 No books in the library.")

elif menu == "Statistics":
    st.header("📊 Library Statistics")
    total, read, percent = manager.display_statistics()
    st.write(f"📚 Total books: {total}")
    st.write(f"✅ Books read: {read} ({percent:.2f}%)")
