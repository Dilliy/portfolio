"""I added few features, as an opportunity to save data after file is finished, as well as to see all books\members saved and disassigning book from member."""


#Libraries
import os
import pickle

#Classes
class library:
    def __init__(self,amount_of_books, number_of_members):
        self.book_amount = amount_of_books
        self.members_amount = number_of_members

    def create_list(self):
        global book_exist
        if book_exist:
            print("List already exist, please use addition.")
        else:
            print("Please, enter book, author and date of creation.\nIf you want to finish enter '1'.")
            stop = False
            index = 0
            while not(stop):
                name = input("Enter Book name: ")
                author = input("Enter author name and surname: ")
                creation_date = input("Enter date of creation: ")
                if name == "1" or author == "1" or creation_date == "1":
                    stop = True
                else:
                    book_name_temp = index
                    book_name_temp = book(name, creation_date, author, False)
                    book_element_index.append(book_name_temp)
                    index += 1
            self.book_amount = index
 
    def add_book(self):
        global book_exist
        if self.book_amount>0:
            print("Please, enter book, author and date of creation.\nIf you want to finish enter '1'.")
            stop = False
            index = self.book_amount
            while not(stop):
                name = input("Enter Book name: ")
                author = input("Enter author name and surname: ")
                creation_date = input("Enter date of creation: ")
                if name == "1" or author == "1" or creation_date == "1":
                    stop = True
                else:
                    book_name_temp = index
                    book_name_temp = book(name, creation_date, author, False)
                    book_element_index.append(book_name_temp)
                    index += 1
                    self.book_amount+=1

        else:
            print("You need to create list at first.")
    
    def delete_book(self):
        global book_exist
        if self.book_amount>0:
            print('Please enter name of the book that you want to delete.\nIf you want to finish please enter "1".')
            stop = False
            while not(stop):
                found = False
                name = input("Please enter the name of the book: ")
                author = input("Please enter author name and surname: ")
                author = author.lower().replace(" ","")
                if name != "1" and author != "1":
                    for i in book_element_index:
                        if i.name == name and i.author.lower().replace(" ","") == author:
                            book_element_index.remove(i)
                            del i
                            found = True
                            self.book_amount -=1
                            if self.book_amount == 0:
                                stop = True
                                book_exist = False
                                try:
                                    path = os.path.realpath("book.pkl")
                                    os.remove(path)
                                    print('Your list has been removed, as all books were deleted.')
                                except:
                                    print('Your list has been removed, as all books were deleted.')
                        else:
                            pass
                    if found:
                        print("Book was deleted")
                    else:
                        print("Book was not found")
                else:
                    stop = True
        else:
            print("You need to create list at first.")
    
    def remove_book_list(self):
        global book_exist
        if book_exist:
            path = os.path.realpath("book.pkl")
            os.remove(path)
            print('Your list has been removed.')
            book_exist = False
            self.book_amount = 0
        else:
            print('You need to create list at first.')

    def print_available(self):
        if self.book_amount>0:
            for i in book_element_index:
                print(f'Name:{i.name}, author:{i.author}, creation_date:{i.creation_date}, book is taken: {i.taken}.')
            print(f"Number of books: {self.book_amount}.")
        else:
            print('You need to create list at first.')

    def new_member(self):
        global member_exist
        print("Please enter initials and date of birthday of the new member: ")
        name = input("Name: ")
        surname = input("Surname: ")
        bd = input("Birthday: ")
        member_index_temp = self.book_amount
        member_index_temp = member(name,surname,bd,[])
        member_element_index.append(member_index_temp)
        self.members_amount += 1
        
    def delete_member(self):
        global member_exist
        if self.members_amount>0:
            print("Please enter Name, Surname and date of birthday to delete member: ")
            name = input("Name: ").lower()
            surname = input("Surname: ").lower()
            bd = input("Birthday: ")
            found = False
            for i in member_element_index:
                if i.name.lower() == name and i.surname.lower() == surname and i.author_bd == bd:
                    member_element_index.remove(i)
                    del i
                    found = True
                    self.members_amount -=1
                    if self.members_amount == 0:
                        member_exist = False
                        try:
                            path = os.path.realpath("members.pkl")
                            os.remove(path)
                            print('Your list has been removed, as all members were deleted.')
                        except:
                            print('Your list has been removed, as all members were deleted.')
                else:
                    pass
            if found:
                print("Member was deleted")
            else:
                print("Member was not found")
        else:
            print("Add at least one member at first")
    
    def remove_member_list(self):
        global member_exist
        if member_exist:
            path = os.path.realpath("members.pkl")
            os.remove(path)
            print('Your list has been removed.')
            member_exist = False
            self.members_amount = 0
        else:
            print("Please, create list at first.")
    
    def assign_book(self):
        if self.book_amount>0 and self.members_amount>0:
            book_list_temp = []
            print("Please write members name and surname, and number of books that you want to assign.")
            m_name = input("Member name: ").lower()
            m_surname = input("Member surname: ").lower()
            b_to_add = int(input("Number of books to add: "))
            member_found = False
            for i in member_element_index:
                if i.name.lower() == m_name and i.surname.lower() == m_surname:
                    print("Member was found")
                    member_found = True
                    index = member_element_index.index(i)
            if member_found:
                for i in range(b_to_add):
                    b_name = input("Enter book name: ")
                    b_author = input("Enter author name and surname: ").lower().replace(" ","")
                    for i in book_element_index:
                        if i.name == b_name and i.author.lower().replace(" ","") == b_author:
                            if i.taken:
                                print("This book is already taken")
                            else:
                                print("Book was found and assigned")
                                book_list_temp.append(i.name)
                                member_element_index[index].book_taken.append(i.name)
                                i.taken = True 
                if len(book_list_temp) != 0:
                    print("All books needed are assigned.")
                else:
                    print("None of books were found and assigned.")

            else:
                print("Member was not found. Please try again")


        elif self.members_amount>0 and not(self.book_amount>0):
            print("Please create book list at first.")

        elif not(self.members_amount>0) and self.book_amount>0:
            print("Please create members list at first.")

        else:
            print("Please create both: list of members and list of books.")
    
    def disassing_book(self):
        if self.book_amount>0 and self.members_amount>0:
            print("Please enter name of the book and author name , to disassign book. ")
            b_name = input("Enter book name: ")
            b_author = input("Enter author name and surname: ").lower().replace(" ","")
            taken = False
            disassigned = False
            not_found = False
            for i in book_element_index:
                if i.name == b_name and i.author == b_author:
                    if i.taken:
                        i.taken = False
                        taken = True
                        index = book_element_index.index(i)
                    else:
                        print("This book is not assigned.")
                else:
                    not_found = True
                    
            if taken:
                for i in member_element_index:
                    try:
                        i.book_taken.remove(book_element_index[index].name)
                        disassigned = True
                    except:
                        pass
                if disassigned:
                    print("Book was disassigned")
                else:
                    print("Something went wrong.")
            elif not(not_found):
                print("This book is not taken.")
            else:
                print("Book was not found.")

        elif self.members_amount>0 and not(self.book_amount>0):
            print("Please create book list at first.")

        elif not(self.members_amount>0) and self.book_amount>0:
            print("Please create members list at first.")

        else:
            print("Please create both: list of members and list of books.")
            
    def print_members(self):
        if self.members_amount>0:
            for i in member_element_index:
                print(f'Name:{i.name}, author:{i.surname}, date of birthd:{i.author_bd}, book taken:{i.book_taken}')
            print(f"Number of members: {self.members_amount}.")
        else:
            print("Please, create member list at first.")

class book:
    def __init__(self, book_name, date_of_creation,author,book_istaken):
        self.name = book_name
        self.creation_date = date_of_creation
        self.author = author
        self.taken = bool(book_istaken)

class member:
     def __init__(self, author_name, author_surname, author_date, book_taken_name):
          self.name = author_name
          self.surname = author_surname
          self.author_bd = author_date
          self.book_taken = book_taken_name

#Global Variables   

library_exist = False
book_exist = False
member_exist = False
stop_main_menu = False
    
library_list_name = []
book_element_index = []
member_element_index = []

#Classes upload
try:
    with open('libraby.pkl', 'rb') as fp:
        library_exist = True
        while(True):
            try:
                library_list_name.append(pickle.load(fp))
            except EOFError:
                break

except:
    print("Please, create library to start. Enter the name for it.")
    library_name = input()
    library_name = library(0,0)
    library_list_name.append(library_name)
    library_exist = True

try:
    with open('book.pkl', 'rb') as fp:
        book_exist = True
        while(True):
            try:
                book_element_index.append(pickle.load(fp))
            except EOFError:
                break
            
except:
    pass

try:
    with open('members.pkl', 'rb') as fp:
        member_exist = True
        while(True):
            try:
                member_element_index.append(pickle.load(fp))
            except EOFError:
                break
        
except:
    pass

#Main body
while not(stop_main_menu):
    print("Enter 1 if you want to create books' list.\nEnter 2 if you want to add books.\nEnter 3 if you want to remove list.\nEnter 4 if you want to delete book.\nEnter 5 if you want to list all books. ")
    print("Enter 6 if you want to create|add member.\nEnter 7 if you delete member.\nEnter 8 if you want to remove member list.\nEnter 9 if you want to assign book.\nEnter 10 if you want to take assigmanet from book.")
    print("Enter 11 if you want to print list of members.")
    try:
        choice = int(input())
        if choice == 1:
            print("Create List\n")
            library_list_name[0].create_list()
        elif choice == 2:
            print("Book addition\n")
            library_list_name[0].add_book()
        elif choice == 3:
            print("Book list remove.\n")
            library_list_name[0].remove_book_list()
        elif choice == 4:
            print("Book delete.\n")
            library_list_name[0].delete_book()
        elif choice == 5:
            print("Book list.\n")
            library_list_name[0].print_available()
        elif choice == 6:
            print("New member.\n")
            library_list_name[0].new_member()
        elif choice == 7:
            print("Member delete.\n")
            library_list_name[0].delete_member()
        elif choice == 8:
            print("Member list remove.\n")
            library_list_name[0].remove_member_list()
        elif choice == 9:
            print("Book assign.\n")
            library_list_name[0].assign_book()
        elif choice == 10:
            print("Book disassing.\n")
            library_list_name[0].disassing_book()
        elif choice == 11:
            print("Member list.\n")
            library_list_name[0].print_members()
        else:
            stop_main_menu = True
    except:
        print("Please, enter digit.")
    

#Classes save
try:
    with open('libraby.pkl', 'wb') as fp:
        for i in library_list_name:
            pickle.dump(i, fp)

except:
    pass

try:
    with open('book.pkl', 'wb') as fp:
        for i in book_element_index:
            pickle.dump(i, fp)

except:
    pass
    

try:
    with open('members.pkl','wb') as fp:
        for i in member_element_index:
            pickle.dump(i,fp)

except:
    pass