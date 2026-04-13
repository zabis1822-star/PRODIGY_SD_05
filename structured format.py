import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox


def scrape_data():
    URL = "http://books.toscrape.com/"
    
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")

        data = []

        for book in books:
            name = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            rating_class = book.find("p", class_="star-rating")["class"]
            rating = rating_class[1]

            data.append((name, price, rating))

        
        for row in tree.get_children():
            tree.delete(row)

        
        for item in data:
            tree.insert("", tk.END, values=item)

        
        df = pd.DataFrame(data, columns=["Name", "Price", "Rating"])
        df.to_csv("products.csv", index=False)

        messagebox.showinfo("Success", "Data scraped and saved to products.csv!")

    except Exception as e:
        messagebox.showerror("Error", str(e))



root = tk.Tk()
root.title("Product Scraper")
root.geometry("700x400")


title_label = tk.Label(root, text="E-commerce Product Scraper", font=("Arial", 16))
title_label.pack(pady=10)


scrape_button = tk.Button(root, text="Scrape Products", command=scrape_data, bg="green", fg="white")
scrape_button.pack(pady=10)


columns = ("Name", "Price", "Rating")
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=200)

tree.pack(expand=True, fill="both", padx=10, pady=10)


root.mainloop()
