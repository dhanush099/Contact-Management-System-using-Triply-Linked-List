import tkinter as tk
from tkinter import messagebox

class ContactNode:
    def __init__(self, name, phone_number):
        self.name = name
        self.phone_number = phone_number
        self.next = None
        self.prev = None
        self.child = None

class ContactList:
    def __init__(self):
        self.head = None

    def add_contact(self, name, phone_number):
        new_contact = ContactNode(name, phone_number)
        if not self.head:
            self.head = new_contact
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_contact
            new_contact.prev = current

    def add_subcontact(self, name, phone_number, parent):
        new_node = ContactNode(name, phone_number)
        parent = self.search_contact(parent)
        if parent.child:
            parent.child.add_contact(name, phone_number)
        else:
            parent.child=ContactList()
            parent.child.head=new_node

    def display_contacts(self):
        current = self.head
        while current:
            print("Name:", current.name)
            print("Phone Number:", current.phone_number)
            print("--------------------")
            if current.child:
                current.child.display_contacts()
            current = current.next

    def search_contact(self, name):
        current = self.head
        while current:
            if current.name == name:
                return current
            if current.child:
                result = current.child.search_contact(name)
                if result:
                    return result
            current = current.next
        return None

    def delete_contact(self, name):
        contact = self.search_contact(name)
        if not contact:
            print("Contact not found!")
            return

        if contact.prev:
            contact.prev.next = contact.next
        else:
            self.head = contact.next

        if contact.next:
            contact.next.prev = contact.prev

        if contact.child:
            contact.child.delete_all_contacts()
            contact.child = None

        print("Contact deleted successfully!")

    def delete_all_contacts(self):
        current = self.head
        while current:
            if current.child:
                current.child.delete_all_contacts()
                current.child = None
            next_contact = current.next
            del current
            current = next_contact
        self.head = None

class ContactManagerUI:
    def __init__(self, contact_list):
        self.contact_list = contact_list

        self.root = tk.Tk()
        self.root.title("Contact Manager")

        self.name_label = tk.Label(self.root, text="Name:")
        self.name_label.pack()

        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        self.phone_label = tk.Label(self.root, text="Phone Number:")
        self.phone_label.pack()

        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.pack()

        self.add_button = tk.Button(self.root, text="Add Contact", command=self.add_contact)
        self.add_button.pack()

        self.parent_label = tk.Label(self.root, text="Parent:")
        self.parent_label.pack()

        self.parent_entry = tk.Entry(self.root)
        self.parent_entry.pack()

        self.name_label = tk.Label(self.root, text="Name:")
        self.name_label.pack()

        self.name1_entry = tk.Entry(self.root)
        self.name1_entry.pack()

        self.phone_label = tk.Label(self.root, text="Phone Number:")
        self.phone_label.pack()

        self.phone1_entry = tk.Entry(self.root)
        self.phone1_entry.pack()

        self.add1_button = tk.Button(self.root, text="Add Sub Contact", command=self.add_subcontact)
        self.add1_button.pack()

        self.delete_label = tk.Label(self.root, text="Enter Name to Delete:")
        self.delete_label.pack()

        self.delete_entry = tk.Entry(self.root)
        self.delete_entry.pack()

        self.delete_button = tk.Button(self.root, text="Delete Contact", command=self.delete_contact)
        self.delete_button.pack()

        self.display_button = tk.Button(self.root, text="Display Contacts", command=self.display_contacts)
        self.display_button.pack()

    def add_contact(self):
        name = self.name_entry.get()
        phone_number = self.phone_entry.get()

        if name and phone_number:
            self.contact_list.add_contact(name, phone_number)
            messagebox.showinfo("Success", "Contact added successfully!")
        else:
            messagebox.showwarning("Error", "Please enter both name and phone number.")

        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

    def add_subcontact(self):
        parent = self.parent_entry.get()
        name = self.name1_entry.get()
        phone_number = self.phone1_entry.get()

        if parent and name and phone_number:
            self.contact_list.add_subcontact(name, phone_number, parent)
            messagebox.showinfo("Success", "Sub Contact added successfully!")
        else:
            messagebox.showwarning("Error", "Please enter both name and phone number.")

        self.parent_entry.delete(0, tk.END)
        self.name1_entry.delete(0, tk.END)
        self.phone1_entry.delete(0, tk.END)

    def delete_contact(self):
        name = self.delete_entry.get()

        if name:
            self.contact_list.delete_contact(name)
            messagebox.showinfo("Success", "Contact deleted successfully!")
        else:
            messagebox.showwarning("Error", "Please enter the name to delete.")

        self.delete_entry.delete(0, tk.END)

    def display_contacts(self):
        contacts_window = tk.Toplevel(self.root)
        contacts_window.title("Contacts")

        scrollbar = tk.Scrollbar(contacts_window)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        contacts_listbox = tk.Listbox(contacts_window, yscrollcommand=scrollbar.set)
        contacts_listbox.pack(fill=tk.BOTH, expand=True)

        current = self.contact_list.head
        while current:
            contacts_listbox.insert(tk.END, f"Name: {current.name}")
            contacts_listbox.insert(tk.END, f"Phone Number: {current.phone_number}")
            contacts_listbox.insert(tk.END, "--------------------")
            if current.child:
                self.display_nested_contacts(current.child, contacts_listbox)
            current = current.next

        scrollbar.config(command=contacts_listbox.yview)

    def display_nested_contacts(self, nested_contact_list, contacts_listbox):
        current = nested_contact_list.head
        while current:
            contacts_listbox.insert(tk.END, f"Name: {current.name}")
            contacts_listbox.insert(tk.END, f"Phone Number: {current.phone_number}")
            contacts_listbox.insert(tk.END, "--------------------")
            if current.child:
                self.display_nested_contacts(current.child, contacts_listbox)
            current = current.next

    def run(self):
        self.root.mainloop()

# Usage example:
contacts = ContactList()
ui = ContactManagerUI(contacts)
ui.run()
