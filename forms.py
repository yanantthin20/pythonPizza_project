from tkinter import *
from tkinter import font
from PIL import Image,ImageTk
from tkinter import messagebox
import socket


orders = {}
subtotal = 0 
# myFont=font.Font(family = 'Times', size = 16)

class Home_frame(Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.header_frame = Frame(self)
        self.body_frame = Frame(self)
        self.order_frame = Frame(self.body_frame, relief='solid', bd=1, width=1000)
        self.total_frame = Frame(self.order_frame)
        global subtotal
        Label(self.order_frame, text = 'Your orders', font = ('Arial', 20)).pack(fill = 'x')
        for o in orders:
            OrderItem_frame(self.order_frame, orders[o]['photo'], o, orders[o]['price'],orders[o]['Small'],orders[o]['Medium'],orders[o]['Large']).pack(side = 'top', anchor = 'w', fill = 'x')
            subtotal += orders[o]['total']
        if subtotal != 0 :
            Button(self.total_frame, text = ' Total ', width = 20, command = self.totalFun).grid(row = 0, column = 0 , sticky = 'w')
            Button(self.total_frame, text = ' Check Out ', width = 20, command = self.checkout).grid(row = 0 , column = 2, padx = 30,sticky = 'e')
        
        self.menu_canvas = Canvas(self.body_frame, width = 600)
        self.sbar = Scrollbar(self.body_frame, command = self.menu_canvas.yview)
        self.menu_canvas.config(yscrollcommand = self.sbar.set)
        self.menu_canvas.bind('<Configure>', lambda e: self.menu_canvas.config(scrollregion = self.menu_canvas.bbox('all')))

        self.menu_canvas.pack(side = 'left', fill = 'both', expand = True, padx = (50, 0))
        self.sbar.pack(side = 'left', fill = 'y')
        self.order_frame.pack(side='left', fill='both', expand=True, padx=(20, 50))
        self.total_frame.pack(side = 'bottom',fill='both', expand=True, padx=(80, 50), pady =(50, 50))
        self.menu_frame = Frame(self.menu_canvas)
        Label(self.header_frame, text = 'Pizza Hut', font = ('Roboto', 20, 'bold', 'italic')).pack()
        self.header_frame.pack(fill = 'x')
        self.body_frame.pack(side = 'left', fill = 'both', expand = True)
        pizzas = [
            [r"images\greekPizza.png", 'Greek Pizza', " Greek Pizza was invented by a Greek from Albania in connection in 1954 . ", 4000,["Olive oil", "leeks", "garlic"]],
            [r"images\margherita.png", 'Margherita Pizza', "Pizza Margherita is a typical Neapolitan pizza", 4500,[" mozzarella cheese", "fresh basil", "olive oil" ]],
            [r"images\newYorkStyle.png", 'New York Style Pizza', "So delicious, The dough is thin and tasty, the ingredients make the pizza even tastier!", 4000,["Dough","Mozzarella","basils"]],
            [r"images\tomatoe.png", 'Tomatoe Pizza', "Far far away, behind the word mountains, far from the countries Vokalia and Consonantia", 4000,["Parmesan cheese","Oregano","Olive Oil"]],
            [r"images\grilledWhite.png", 'Grilled White Pizza', "A simple recipe for Grilled White Pizza loaded with 3 cheese, fresh basil, mushrooms and onions!", 4000,["Basil","Parmesan","Red Pepper"]],
            [r"images\hawaii.png", 'Hawaii Pizza', "also known as pineapple pizza, is a pizza topped with pineapple,harm,tomato sauce and cheese", 4000,["Mozzarella","Pepper jack cheese","Basil"]],
            [r"images\bacon.png", 'Bacon Pizza', "Far far away, behind the word mountains, far from the countries Vokalia and Consonantia", 4000,["Olive oil","Basil","Cheddar cheese"]],
            [r"images\pizza_01.png", 'American Pizza', "Far far away, behind the word mountains, far from the countries Vokalia and Consonantia", 4000,["Olive oil","Basil","Cheddar cheese"]],
            # [r"D:\Projects\kbtc_project\New folder (2)\Pizza order\images\pizza_01.png", 'Italian Pizza', "Far far away, behind the word mountains, far from the countries Vokalia and Consonantia", 2.5,[]],
            # [r"D:\Projects\kbtc_project\New folder (2)\Pizza order\images\pizza_01.png", 'Tomatoe Pie', "Far far away, behind the word mountains, far from the countries Vokalia and Consonantia", 5.5,[]],
            # [r"D:\Projects\kbtc_project\New folder (2)\Pizza order\images\pizza_01.png", 'American Pizza', "Far far away, behind the word mountains, far from the countries Vokalia and Consonantia", 20.2,[]],
            # [r"D:\Projects\kbtc_project\New folder (2)\Pizza order\images\pizza_01.png", 'American Pizza', "Far far away, behind the word mountains, far from the countries Vokalia and Consonantia", 20.2,[]],
        ]
        row = column = 0
        for photo, name, desc, price,ingredients in pizzas:
            Pizza_frame(self.menu_frame, photo, name, desc, price, ingredients).grid(row = row // 2, column = column % 2, padx = 8, pady = 5)
            row += 1
            column += 1

        self.menu_canvas.create_window((0, 0), window=self.menu_frame)
        
    def totalFun(self):
        self.total_frame.pack_forget()
        global subtotal
        subtotal = 0
        for o in orders:
            subtotal += orders[o]['total']
        Label(self.total_frame, text=f"MMK {subtotal} ").grid(row = 0, column = 1, padx=5, sticky = 'w')
        self.total_frame.pack(side = 'bottom',fill='both', expand=True, padx=(80, 50), pady =(50, 50))

    def checkout(self):
       self.body_frame.pack_forget()
       self.order_frame.pack_forget()
       self.total_frame.pack_forget()
       Checkout_Frame(self).pack(side = 'top',fill='both', expand=True, padx=(80, 50), pady =(50, 50))
       

class Pizza_frame(Frame):
    def __init__(self, parent, photo, name, desc, price, ingredients):
        self.parent = parent
        self.photo = photo
        self.name = name
        self.desc = desc
        self.price = price
        self.ingredients = ingredients
        super().__init__(parent)
        self.photo_frame = Frame(self)
        self.desc_frame = Frame(self)
        self.pizza_img = PhotoImage(file = photo)
        Label(self.photo_frame, image = self.pizza_img).pack()
        Label(self.desc_frame, text = name).pack()
        Label(self.desc_frame, text = desc, wraplength = 110, justify = 'left').pack()
        Label(self.desc_frame, text = f"MMK {price}").pack(side = 'left')
        Button(self.desc_frame, text = ' Order ', width = 15, bg="yellow",command = self.goto_detail).pack(side = 'left')
        self.photo_frame.pack(side = 'left', fill = 'y')
        self.desc_frame.pack(side = 'left', fill = 'y')

    def goto_detail(self):
        self.master.master.master.pack_forget()
        Detail_frame(self.master.master.master.master, self.photo, self.name, self.desc, self.price, self.ingredients).pack()

class Detail_frame(Frame):
    def __init__(self, parent, photo, name, desc, price, ingredients):
        self.parent = parent
        self.photo = photo
        self.name = name
        self.price = price
        self.ingredients = ingredients
        self.choice = StringVar()
        self.choice1 = StringVar()
        self.choice2 = StringVar()
        self.Small = "0"
        self.Medium = "0"
        self.Large = "0"
        super().__init__(parent)
        self.desc_frame = Frame(self)
        self.order_frame = Frame(self)
        self.pizza_img = PhotoImage(file = photo)
        self.photo_frame = Frame(self.desc_frame)
        Label(self.photo_frame, image = self.pizza_img).pack(side = 'left', anchor = 'n')
        Button(self.photo_frame, command = self.goto_menu, relief = 'raised', bd = 1, text = 'back to menu...').pack(side = 'right', anchor = 's', padx = (200, 0))
        self.photo_frame.pack(side = 'top', anchor = 'w')
        Label(self.desc_frame, text = name, font = ('Times',15)).pack(side = 'top', anchor = 'w')
        Label(self.desc_frame, text = desc, font = ('Times',15)).pack(side = 'top', anchor = 'w')
        Label(self.desc_frame, text = "Options and extras",font = ('Times',15)).pack(side = 'top', anchor = 'w')
        Label(self.desc_frame, text="Select the ingredients that you dislike.", font=('Times', 15)).pack(side='top', anchor='w')
            
        Checkbutton(self.desc_frame, text = ingredients[0], variable = self.choice, onvalue = ingredients[0]+"|", offvalue = "", font=('Times', 15)).pack(side='top', anchor='w')
        Checkbutton(self.desc_frame, text = ingredients[1], variable = self.choice1, onvalue = ingredients[1]+"|", offvalue = "", font=('Times', 15)).pack(side='top', anchor='w')
        Checkbutton(self.desc_frame, text = ingredients[2], variable = self.choice2, onvalue = ingredients[2]+"|", offvalue = "", font=('Times', 15)).pack(side='top', anchor='w')


        # self.combo = ttk.Combobox(self.desc_frame, values=["Small", "Medium", "Large"])
        # self.combo.pack(side="top", anchor = "w")
        self.optionValue = StringVar()
        self.optionValue.set("Small")
        option = OptionMenu(self.order_frame, self.optionValue, "Small", "Medium", "large")
        option.config(width=25)
        option.pack(side = 'top', anchor = "w")
        self.count = Spinbox(self.order_frame, from_ = 1, to = 100, width = 15)
        self.count.pack(side = 'left', fill = 'y')
        Button(self.order_frame, text = 'Order Now', command = self.order_pizza).pack(side = 'left', padx = (10, 0))
        self.desc_frame.pack()
        self.order_frame.pack(fill='x')
        
    def get_choice(self):
        pass



    def goto_menu(self):
        print('going to menu...')
        self.master.pack_forget()
        Home_frame(self.master.master).pack(fill = 'both', expand = True)

    def order_pizza(self):
        lists = self.choice.get() +self.choice1.get() + self.choice2.get()

        if self.name in orders:
            orders[self.name]['ingredients'] = orders[self.name]['ingredients'] + lists
            if self.optionValue.get() == "Small":
                orders[self.name]['Small'] = str(int(orders[self.name]['Small']) + int(self.count.get()))
                
            elif self.optionValue.get() == "Medium":
                orders[self.name]['Medium'] = str(int(orders[self.name]['Medium']) + int(self.count.get()))
               
            else:
                orders[self.name]['Large'] = str(int(orders[self.name]['Large']) + int(self.count.get()))
               
        else:
            
            # orders[self.name] = {'photo':self.photo, 'price':self.price, 'count':self.count.get(), 'ingredients':lists}}
            orders[self.name] = {'photo':self.photo, 'price':self.price, 'ingredients':lists} 
            if self.optionValue.get() == "Small":
                orders[self.name]['Small'] = self.count.get()
                orders[self.name]['Large'] = "0"
                orders[self.name]['Medium'] ="0"
            elif self.optionValue.get() == "Medium":
                orders[self.name]['Medium'] = self.count.get()
                orders[self.name]['Small'] = "0"
                orders[self.name]['Large'] = "0"
            else:
                orders[self.name]['Large'] = self.count.get()
                orders[self.name]['Medium'] = "0"
                orders[self.name]['Small'] = "0"

           

class OrderItem_frame(Frame):
    def __init__(self, parent, photo, name, price, Small, Medium, Large):
        self.parent = parent
        self.photo = photo
        self.name = name
        self.price = price
        self.Small = Small
        self.Medium = Medium
        self.Large = Large
        super().__init__(parent)
        self.desc_frame = Frame(self)
        self.total_frame = Frame(self)
        self.pizza_img = ImageTk.PhotoImage(Image.open(photo).resize((60, 70)))
        Label(self.desc_frame, image = self.pizza_img).grid(row = 0, column = 0, rowspan = 2)
        Label(self.desc_frame, text=name).grid(row=0, column=1, sticky='w')
        # if optionValue == "Small":
        #     Label(self.desc_frame, text=f"{count} x ${price}").grid(row=1, column=1, sticky='w')
        # elif optionValue == "Medium":
        #      Label(self.desc_frame, text=f"{count} x ${int(price)*2}").grid(row=1, column=1, sticky='w')
        # else:
        #      Label(self.desc_frame, text=f"{count} x ${int(price)*3}").grid(row=1, column=1, sticky='w')
        Label(self.desc_frame, text=f"Small:{Small}x{int(price)}/ Medium:{Medium}x{int(price)*2}/ Large:{Large}x{int(price)*3}").grid(row=1, column=1, sticky="w")
        # calculate total value
        total = int(Small) * 4000 + int(Medium) * 8000 + int(Large) * 12000
        orders[name]['total'] = total

        Label(self.desc_frame, text = f"     =     {total} ").grid(row=1, column=2, padx=12, sticky='e')
        

        self.desc_frame.pack(side='left')
        # Label(self.desc_frame, text = optionValue).grid(row = 0, column = 2, sticky = 'w')
        Button(self, text = 'Remove', bg = 'red',  width=20, height=2, command = self.remove_item).pack(side = 'right', anchor = 'e')
        

    def remove_item(self):
        orders.pop(self.name)
        self.pack_forget()

class Checkout_Frame(Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.addressFrame = Frame(self)
        self.buttonFrame = Frame(self.addressFrame)
        Label(self.addressFrame,text='Name:', font = ('Times',16)).grid(row=0,column=0,padx=30,pady=5)
        self.name=Entry(self.addressFrame,width=30,bg='yellow')
        self.name.grid(row=0,column=1)

        Label(self.addressFrame,text='Contact Number', font = ('Times',16)).grid(row=1,column=0,padx=30,pady=5)
        self.contact_number=Entry(self.addressFrame,width=30,bg='yellow')
        self.contact_number.grid(row=1,column=1)

        Label(self.addressFrame,text='Email :', font = ('Times',16)).grid(row=2,column=0,padx=30,pady=5)
        self.email=Entry(self.addressFrame,width=30,bg='yellow')
        self.email.grid(row=2, column=1)
        
        Label(self.addressFrame,text=' Address', font = ('Times',16)).grid(row=3,column=0,padx=30,pady=5)
        self.address1=Text(self.addressFrame, width= 26, height = 3, bg='yellow')
        self.address1.grid(row=3, column=1)

        Button(self.buttonFrame,text=' Submit ', font = ('Times','11'), width = 10, cursor='heart', command = self.orderSend).pack(side='right')
        Button(self.buttonFrame,text='Reset ', font = ('Times','11'), width = 10,  cursor='heart', command = self.reset).pack(side='right',padx = 10, pady = 5)
        self.buttonFrame.grid(row=5,column=1,sticky='e')
        self.addressFrame.pack(side='top')

    def reset(self):
        self.name.delete(0,END)
        self.contact_number.delete(0,END)
        self.email.delete(0,END)
        self.address1.delete('1.0',END)

    def orderSend(self):
        customerinfo =f"Name :{self.name.get()} | phoneNo :{self.contact_number.get()} | Email:{self.email.get()} | Address :{self.address1.get('1.0','end-1c')}"
        orders['customerinfo'] = customerinfo
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((socket.gethostname(), 1239))
        d = str(orders) 
        def ts(str):
            s.send(d.encode())
            data = ''
            data = s.recv(1024).decode()
            if data != '':
                messagebox.showinfo("Thank you ","Your orders have successfully comfirmed.\nThank you so much for your orders.\nHave a nice day")
        # while 1:
        ts(s)
        s.close ()


