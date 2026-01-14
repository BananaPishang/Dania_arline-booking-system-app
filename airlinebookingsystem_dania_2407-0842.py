# airline booking sytem with tkinter

import tkinter as tk
from tkinter import messagebox

windows = tk.Tk()
windows.title("Airline Booking System")

class SeatBooking:
    def __init__(self, name, seat, age, gender, contact):
        self.name = name
        self.seat = seat
        self.age = age
        self.gender = gender
        self.contact = contact

class ReservationSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Airline Booking System")
        self.root.configure(bg="lightgreen")
        self.bookings = {}
        self.seat_buttons = {}

        # passenger details
        tk.Label(root, text="Name:").grid(row=0, column=0)
        self.name_entry = tk.Entry(root)
        self.name_entry.grid(row=0, column=1)

        tk.Label(root, text="Age:").grid(row=1, column=0)
        self.age_entry = tk.Entry(root)
        self.age_entry.grid(row=1, column=1)

        tk.Label(root, text="Gender:").grid(row=2, column=0)
        self.gender_entry = tk.Entry(root)
        self.gender_entry.grid(row=2, column=1)

        tk.Label(root, text="Contact:").grid(row=3, column=0)
        self.contact_entry = tk.Entry(root)
        self.contact_entry.grid(row=3, column=1)

        # seat map
        seat_frame = tk.LabelFrame(root, text="Seat Map") 
        seat_frame.grid(row=4, column=0, columnspan=3, pady=10)
        seats = [["A1","A2","A3","A4","A5"],["B1","B2","B3","B4","B5"]]
        for r,row in enumerate(seats):
            for c,seat in enumerate(row):
                btn = tk.Button(seat_frame, text=seat, width=6, bg="green",
                                command=lambda s=seat: self.book_seat(s))
                btn.grid(row=r,column=c)
                self.seat_buttons[seat] = btn

        #booking list
        tk.Label(root, text="Booking List:").grid(row=5, column=0, sticky="w")
        self.booking_list = tk.Listbox(root, width=50, height=6)
        self.booking_list.grid(row=6, column=0, columnspan=3)

        # cancel and search
        tk.Button(root, text="Cancel Booking", bg="red", command=self.cancel_booking).grid(row=7, column=1, pady=5)
        tk.Label(root, text="Search:").grid(row=8, column=0, sticky="w")
        self.search_entry = tk.Entry(root)
        self.search_entry.grid(row=8, column=1)
        tk.Button(root, text="Search", bg="orange", command=self.search_booking).grid(row=8, column=2)

        self.load_bookings()

    def load_bookings(self):
        try:
            with open("booking.txt","r") as f:
                for line in f:
                    seat,name,age,gender,contact = line.strip().split(",")
                    self.bookings[seat]=SeatBooking(name,seat,age,gender,contact)
                    self.seat_buttons[seat].config(bg="red",state="disabled")
                    self.booking_list.insert(tk.END,f"{name} - Seat {seat}")
        except FileNotFoundError:
            pass

    def save_bookings(self):
        with open("booking.txt","w") as f:
            for seat,b in self.bookings.items():
                f.write(f"{seat},{b.name},{b.age},{b.gender},{b.contact}\n")

    def book_seat(self, seat):
        name=self.name_entry.get().strip()
        age=self.age_entry.get().strip()
        gender=self.gender_entry.get().strip()
        contact=self.contact_entry.get().strip()
        if not (name and age and gender and contact):
            messagebox.showwarning("Input Error","Please fill all fields!")
            return
        if seat in self.bookings:
            messagebox.showwarning("Seat Taken",f"Seat {seat} is already booked.")
            return
        self.bookings[seat]=SeatBooking(name,seat,age,gender,contact)
        self.seat_buttons[seat].config(bg="red",state="disabled")
        self.booking_list.insert(tk.END,f"{name} - Seat {seat}")
        self.save_bookings()
        self.name_entry.delete(0,tk.END)
        self.age_entry.delete(0,tk.END)
        self.gender_entry.delete(0,tk.END)
        self.contact_entry.delete(0,tk.END)

    def cancel_booking(self):
        selected=self.booking_list.curselection()
        if not selected:
            messagebox.showwarning("Selection Error","Please select a booking to cancel.")
            return
        seat=self.booking_list.get(selected[0]).split("Seat ")[1]
        del self.bookings[seat]
        self.seat_buttons[seat].config(bg="green",state="normal")
        self.booking_list.delete(selected[0])
        self.save_bookings()

    def search_booking(self):
        query=self.search_entry.get().strip().lower()
        if not query:
            messagebox.showwarning("Input Error","Enter a name or seat to search.")
            return
        for seat,b in self.bookings.items():
            if query in b.name.lower() or query in seat.lower():
                messagebox.showinfo("Found",f"Name:{b.name}\nSeat:{b.seat}\nAge:{b.age}\nGender:{b.gender}\nContact:{b.contact}")
                return
        messagebox.showinfo("Not Found","No booking found.")

if __name__=="__main__":
    root=tk.Tk()
    app=ReservationSystemGUI(root)
    root.mainloop()
    windows.mainloop()
