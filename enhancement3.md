[Home](README.md) -- [Code Review](CodeReview.md) -- [Enhancement One](enhancement1.md) -- [Enhancement Two](enhancement2.md) -- [Enhancement Three](enhancement3.md)

# Narrative
<p>This artifact is an evolution and addition to the program I converted from Java into Python for enhancement one for my CS-499 capstone project, further enhanced by enhancement two. Enhancement three focuses on creating a database to store information for the pet boarding system. Using MongoDB and importing pymongo into the Python file allowed me to create a database for persistent data storage and improve the functionality of various methods already in place. The check-in and check-out methods are now integrated into the database system to store and retrieve information on boarded pets. Space availability has been moved to the database system entirely and is tracked by the database itself, adding or subtracting spaces during the check-in and check-out processes respectively. I realized during the creation of the database system that there was no way to identify pets with the same name. To remedy this problem, I added owner information management to collect the pet owner’s information such as their email, phone number, and a unique identifier to tie the owner to a specific pet. The owner's email is always processed first before the pet name to ensure the owner is processing the correct pet during pet check-in/out or when accessing pet boarding history. I also added an option in the menu of the program for pet boarding history which allows a pet owner to see all past information on their pet(s) if they have used the service before.</p>

<p>Including this artifact demonstrates that I understand how to design and integrate a database system for an application by creating a MongoDB database for persistent storage with proper indexing for queries and error handling which also provides data relationship management between pets and their owners. Enhancement three also demonstrates an understanding of security and data integrity through owner verification, email validation, and unique ID generation along with proper input validation techniques. The original code from enhancement one has been significantly improved with the addition of a database that provides persistent data storage that was missing from the original program. The original program stores all information in system memory that is lost upon terminating the application whereas database storage saves all information and stores it in the database for future use, pet boarding application running or not.</p>

<p>Enhancement three successfully meets the course outcomes that I planned on demonstrating. I had met all previous course outcomes with previous enhancements, so I was only focused on developing a security mindset, which I achieved through owner verification, data relationships, error handling, and data validation. However, upon further review of the course outcomes, I noticed that creating a database for this program also demonstrates other course outcomes as well. I designed a computing solution that solved the problem of data persistence by implementing new data structures and algorithms for pet management in a database environment where data can persist. I also demonstrated my ability to use well-founded techniques, skills, and tools by integrating a MongoDB database system with an existing Python program. Additionally, this enhancement also demonstrates that I can clearly document a program's functions with the use of comments explaining what each section of the code does.</p>

<p>This was by far the most challenging enhancement of the capstone project because I encountered many issues trying to get the database up and running. I had never set up a database on my own because the database environments were already set up in most courses throughout my time at SNHU through virtual machines. I wish that all classes at SNHU gave you the option to set up your own environment to help you understand the process. Anyway, after I had finally got the database set up, I distinctly remember that my biggest hurdle was retrieving data from the database. I was stuck for the longest time because I could write to the database and save the information (verified by querying) but when I would try to check-out a pet or view a pet's history, the program could not find the data (even though I was staring right at it in another window). Finally, I noticed that my create_pet_record method had no usage within the code itself so I was able to write data to the database, but since I did not call it within the save_pet_checkin method the data was unreachable when trying to look for it because I did not create the link between pets and their boarding history. I feel like I learned a lot more about the concepts taught to me in previous classes by essentially starting from scratch for enhancement one and using the same program for each subsequent enhancement for my capstone project and I think that helps to demonstrate a well-rounded understanding of programming logic and the process of development.</p>

# Databases
## Main Program
```
"""
Author: Rob Crowe
Email: robert.crowe@snhu.edu
Class: CS-499 Capstone
Purpose: Capstone Project Enhancement 3 - Databases

Title: Pet Boarding Program

This program is the continuation of the Pet boarding program which I converted from
Java for enhancement 1 of my capstone project and includes all enhancements made for enhancement 2.
Enhancement 3 further expands the functionality of my pet boarding program by creating a database to
store information on the pets to have a record of all pets.

This enhancement adds functionality to include owner information, pet records, pet history, and
finally includes methods to update pet information. All made possible by the inclusion of database
integration. I needed to include owner information to ensure that the correct pet was being processed
in the event of pets having the same name. Tying owner information to a pet during the check-in process
and giving them a unique id ensures the correct pet is being chosen during the check-out process.
"""

# importing the PetDatabase class from Pet_Database.py
from Pet_Database import PetDatabase
import datetime # imports date and time information

class Pet:
    """
    The Pet class represents a pet for the boarding program and handles all pet and owner
    information for the check-in and check out-processes including saving and retrieving information
    from the database.

    Enhancement 3:
    You will notice commented out sections which remain there to show methods and functions used
    during previous iterations of this program. I left them in to show progress was made during the
    evolution of this project. The methods and functions are not needed anymore for this version
    because they are now handled by the database.
    """

    # dictionaries for cat and dog spaces
    #SPACES = {
        #'cat': {'total': 12, 'available': 12},
        #'dog': {'total': 30, 'available': 30}
    #}

    # dictionaries for pricing cats and dogs which includes the dogs weight category
    PRICING = {
        'cat': {
            'daily_rate': 18.00,
            'grooming': None # Cats groom themselves, no grooming services available
        },

        'dog': {
            'large': { # 30+ lbs
                'daily_rate': 34.00,
                'grooming': 29.95
            },
            'medium': { # 20-29 lbs
                'daily_rate': 29.00,
                'grooming': 24.95
            },
            'small': { # under 20 lbs
                'daily_rate': 24.00,
                'grooming': 19.95
            }
        }
    }

    def __init__(self, pet_type="", pet_name="", pet_age=0, days_stay=0, amount_due=0):
        """
        Initialize the pet instance with default values
        (petType=string, petName=string, petAge=int, daysStay=int, amount_due=int)

        Enhancement 3:
        adds default values for owner info_and calls the database
        """
        self.pet_type = pet_type
        self.pet_name = pet_name
        self.pet_age = pet_age
        #self.dog_space = dog_space
        #self.cat_space = cat_space
        self.days_stay = days_stay
        self.amount_due = amount_due
        self.dog_weight = 0 # used to determine pricing
        self.grooming_service = False # set to false by default, tracks if grooming services requested
        self.daily_rate = 0 # stores the daily boarding rate
        self.grooming_fee = 0 # stores the grooming fee
        self.dog_size_category = None

        # enhancement 3 additions
        self.owner_info = None
        self.db = PetDatabase()

    def collect_owner_info(self):
        """
        Enhancement 3:
        Collects information about the pets owner to ensure correct pet processing by tying the owners
        information to the pets information during the check-in, check-out and pet history processes
        """

        print("Please provide owner information: ")
        while True:
            email = input("Email address: ").strip()
            if '@' in email and '.' in email: # ensure a valid email address is entered
                break
            print("Please enter a valid email address.")

        # collect owner information
        owner_info = {
            'email': email,
            'name': input("Owner's name: ").strip(),
            'phone': input("Phone number: ").strip()
        }
        self.owner_info = owner_info
        return owner_info


    def check_in(self):
        """
        Handle the check-in process for a pet, determine space availability,
        gather pet information, and gather owner information

        Enhancement 3:
        Adds functionality to collect owner information, save all information to the database, and
        update the available spaces in the database
        """

        while True:
            # print welcome message
            print("Welcome, are you checking in a cat or dog?:")
            pet_type = input().lower()  # set all input to lowercase for comparison

            space = self.db.get_available_space()

            if pet_type in ['cat', 'dog']:
                self.pet_type = pet_type
                if space[pet_type] > 0:
                    # collect owner information first
                    owner_info = self.collect_owner_info()
                    # then check in the pet
                    self._pet_checkin()
                    # save all information to the database
                    self.db.save_pet_checkin(self, owner_info)
                    self.db.update_spaces(pet_type, checking_in=True)
                    break
                else:
                    print(f"Sorry, there are no {pet_type} spaces available.")
                break
            else:
                print("Invalid input, Please enter 'cat' or 'dog'")

    def _pet_checkin(self):
        """
        This function handles the check in process for all pets based on type and will call to the
        appropriate functions, cat or dog, respectively.
        """
        print(f"{self.pet_type} space is available!")
        print("Is your pet a new or returning visitor?")

        while True:
            visitor_type = input().lower()
            if visitor_type == "new":
                if self.pet_type == "cat":
                    self._new_cat_info()
                else:
                    self._new_dog_info()
                break
            elif visitor_type == "returning":
                if self.pet_type == "cat":
                    self._returning_cat_info()
                else:
                    self._returning_dog_info()
                break
            else:
                print("Please enter either 'new' or 'returning'.")

    def _new_cat_info(self):
        """
        This function gathers information on new cats including the daily fee for boarding a cat,
        calculating the fees, and printing the receipt.
        """
        # collect information for the new cat visitor
        print("Welcome to new cat registration")
        print("        ^._.^= ∫         ")
        print("\nWhat is your cats name?: ")
        self.pet_name = input()
        print("How old is your cat?: ")
        self.pet_age = int(input()) # will only accept an integer as the input
        print("How many days will your cat be staying?: ")
        self.days_stay = int(input()) # will only accept an integer as the input

        # set cat pricing, calculate fees, and print receipt
        self._set_pricing()
        self.calculate_fees()
        self.print_receipt()


    def _returning_cat_info(self):
        """
        Handles returning cat information

        Enhancement 3:
        Looks in the database for if the pet has visited before. If the pet is not found in the database
        the method asks if the owner would like to register as a new cat. If the pet is found in the
        database the method displays the previous pet visit information then asks to update pet information.
        the method also asks how long the cat will be staying and sets the pricing, calculates fees,
        updates the pets information in the database, and prints the receipt for the visit.
        """
        # collect information for a returning cat
        print("Welcome back! Lets update the information on your cat.")

        print("What is your cats name?")
        cat_name = input()
        history = self.pet_history(cat_name)

        # if the pet is not found in the database
        if not history:
            print("We could not find any records with that name.")
            # ask to register as a new pet
            print("Would you like to register as a new cat instead (yes/no)")
            answer = input().lower()
            # if input is 'yes'
            if answer == 'yes':
                # call _new_cat_info method
                self._new_cat_info()
                return
            else:
                print("Check the name and try again.")
                return

        # set pet name to cat name and pet type to cat
        self.pet_name = cat_name
        self.pet_type = 'cat'

        # if there is a record of the cat in the database print out previous visit information
        pet_info = history[0]['pet_info']
        print("Previous visit information")
        print(f"Name: {cat_name}")
        print(f"Age on last visit: {pet_info.get('age', 0)}")

        # ask to update cat age
        print("Would you like to update your cats age? (yes/no)")
        update_age = input().lower()
        # if update_age is yes
        if update_age == 'yes':
            while True:
                try:
                    # ask for input for cats current age
                    print("Please enter your cats age: ")
                    self.pet_age = int(input()) # will only accept an integer as the input
                    if self.pet_age < 0:
                        print("Age cannot be negative.")
                        continue
                    break
                except ValueError:
                    print ("Please enter a valid age.")
        else:
            self.pet_age = pet_info.get('age', 0)

        while True:
            try:
                # ask for length of stay
                print("How many days will your cat be staying?: ")
                self.days_stay = int(input()) # will only accept an integer as the input
                if self.days_stay <= 0:
                    print("Stay duration must be at least 1 day.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number")


        # set cat pricing, calculate fees, update pet record in database, and print receipt
        self._set_pricing()
        self.calculate_fees()

        self.db.update_pet_record(
            self.pet_name,
            {
                'age': self.pet_age,
                'days_stay': self.days_stay,
                'amount_due': self.amount_due,
                'last_updated': datetime.datetime.now()
            }
        )

        self.print_receipt()

    def _new_dog_info(self):
        """
        This function gathers information on new dogs including the daily fee for boarding a dog,
        check grooming eligibility, calculating the fees, and printing the receipt.
        """
        # collect information on the new dog visitor
        print("Welcome to new dog registration!")
        print("         (❍ᴥ❍ʋ)         ")
        print("\nWhat is your dogs name?: ")
        self.pet_name = input()
        print("How old is your dog?: ")
        self.pet_age = int(input())
        print("Please enter your dogs weight in pounds")
        self.dog_weight = float(input())
        print("How many days will your dog be staying?: ")
        self.days_stay = int(input())

        # determine price, check if eligible for grooming service, calculate fees, print receipt
        self._set_pricing()
        self._grooming_eligible()
        self.calculate_fees()
        self.print_receipt()

    def _returning_dog_info(self):
        """
        This function handles information for a returning dog

        Enhancement 3:
        Looks in the database for if the pet has visited before. If the pet is not found in the database
        the method asks if the owner would like to register as a new dog. If the pet is found in the
        database the method displays the previous pet visit information then asks to update pet information.
        the method also asks how long the dog will be staying and sets the pricing, calculates fees,
        updates the pets information in the database, and prints the receipt for the visit.
        """
        print("Welcome back! Lets update the information on your dog.")

        print("What is your dogs name?")
        dog_name = input()
        history = self.pet_history(dog_name)

        # if the dog is not found in the database ask to register as a new dog
        if not history:
            print("We could not find any records with that name.")
            print("Would you like to register as a new dog instead (yes/no)")
            answer = input().lower()
            if answer == 'yes':         # if yes
                self._new_dog_info()    # call _new_dog_info method
                return
            else:
                print("Check the name and try again.")

                return

        # set pet_name to dog_name and pet_type to dog
        self.pet_name = dog_name
        self.pet_type = 'dog'

        # if the pet is found in the database, display previous visit information
        pet_info = history[0]['pet_info']
        print("Previous visit information")
        print(f"Name: {dog_name}")
        print(f"Age on last visit: {pet_info.get('age', 0)}")
        print(f"Previous weight: {pet_info.get('weight', 0)} lbs")

        # asks to update dogs age
        print("Would you like to update your dogs age? (yes/no)")
        update_age = input().lower()
        # if update_age is yes
        if update_age == 'yes':
            while True:
                try:
                    # ask for age input
                    print("Please enter your dogs age: ")
                    self.pet_age = int(input()) # set input to integer
                    if self.pet_age < 0:
                        print("Age cannot be negative.")
                        continue
                    break
                except ValueError:
                    print("Please enter a valid age.")
        else:
            self.pet_age = pet_info.get('age', 0)

        while True:
            try:
                # confirm the dogs weight
                print("Please confirm your dogs weight in pounds: ")
                self.dog_weight = float(input()) # set input to float
                if self.dog_weight <= 0:
                    print("Weight must be greater than 0.")
                    continue
                break
            except ValueError:
                print("Please enter a valid weight.")

        while True:
            try:
                # ask for length of stay
                print("How many days will your dog be staying?: ")
                self.days_stay = int(input())  # will only accept an integer as the input
                if self.days_stay <= 0:
                    print("Stay duration must be at least 1 day.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number")

        # determine price, check if eligible for grooming service, calculate fees,
        # update the pets record in database, and print receipt
        self._set_pricing()
        self._grooming_eligible()
        self.calculate_fees()

        self.db.update_pet_record(
            self.pet_name,
            {
                'age': self.pet_age,
                'weight': self.dog_weight,
                'days_stay': self.days_stay,
                'amount_due': self.amount_due,
                'grooming_service': self.grooming_service,
                'last_updated': datetime.datetime.now()
            }
        )

        self.print_receipt()

    def _determine_dog_size(self):
        """
        Determines which weight category a dog will be assigned based on their weight
        """
        if self.dog_weight >= 30:
            return "large"
        elif self.dog_weight >=20:
            return "medium"
        else:
            return "small"

    def _set_pricing(self):
        """
        Sets the daily rate and grooming fee (if applicable) based on pet type and size
        """
        # if pet type is cat set the daily rate by pulling information from the pricing dictionary
        if self.pet_type == 'cat':
            self.daily_rate = self.PRICING['cat']['daily_rate']
            self.grooming_fee = 0   # set grooming fee to zero for cats
        # else the pet type is a dog
        else:
            self.dog_size_category = self._determine_dog_size() # determine size category of the dog
            # set the price and pull price information from the pricing dictionary
            price = self.PRICING['dog'][self.dog_size_category]
            self.daily_rate = price['daily_rate']
            self.grooming_fee = price['grooming']

    def _grooming_eligible(self):
        """
        This function will handle checking to see if a dog is eligible for grooming services
        based on their days stay.
        """
        if self.days_stay >= 2:
            print("grooming services are available for your dog!")
            # using a formatted string, pull the information from the pricing dictionary
            print(f"The grooming fee is: ${self.grooming_fee:.2f}")

            # while days stay is greater than 2 ask if the customer wants grooming services
            while True:
                print("Would you like to add a grooming service? (yes/no)")
                answer = input().lower()

                # if the customer wants grooming services
                if answer == 'yes':
                    # set grooming service to true
                    self.grooming_service = True
                    # print confirmation message
                    print("Grooming service added")
                    break
                # if the customer does not want grooming services
                elif answer == 'no':
                    # set grooming service to false
                    self.grooming_service = False
                    print("Grooming service not added")
                    break
                # input validation to ensure correct words are input
                else:
                    print("Please enter 'yes' or 'no'.")
        else:
            print("Grooming is not available for your dog.")

    #def check_available_space(self, pet_type):
       # """
       # enhancement 2:
       # Checks if there is currently available space for the pet_type entered by pulling
       # information from the spaces dictionary
       # """
        #return self.SPACES[pet_type]['available'] > 0

    # def update_space_count(self, pet_type, checking_in=True):
    #     """
    #     enhancement 2:
    #     Update the space count during check-in or check-out, the dictionary will update according
    #     to the check in (subtract 1 space) or check out (add 1 space back) process
    #     """
    #     if checking_in:
    #         self.SPACES[pet_type]['available'] -= 1
    #     else:
    #         self.SPACES[pet_type]['available'] += 1

    def calculate_fees(self):
        """
        Calculate the total fees based on length of stay and services chosen
        """
        # calculate boarding cost without additional service
        self.amount_due = self.daily_rate * self.days_stay

        # adding additional grooming fee if applicable
        if self.grooming_service:
            self.amount_due += self.grooming_fee

    def print_receipt(self):
        """
        Generates a receipt to show stay information and the total cost to the owner using
        formatted strings to pull in relevant information
        """
        # display pets name, type, and length of stay depending on the input
        print(f"Pet Name: {self.pet_name}")
        print(f"Pet Type: {self.pet_type.capitalize()}")
        print(f"Length of stay: {self.days_stay} days")

        # if the pet type is a dog, print out relevant information
        if self.pet_type == "dog":
            print(f"Weight Category: {self._determine_dog_size()}")
            print(f"Boarding Rate: ${self.daily_rate:.2f}/day")

            if self.grooming_service:
                print(f"Grooming service: ${self.grooming_fee:.2f}")
        # if the pet type is a cat, print out relevant information
        else:
            print(f"Cat Boarding: ${self.daily_rate:.2f}/day")

        # print out the total boarding fee
        print(f"Total Boarding: ${(self.daily_rate * self.days_stay):.2f}")
        # if a grooming fee is added on for a dog, add the grooming fee to the receipt
        if self.grooming_service:
            print(f"Grooming fee: ${self.grooming_fee:.2f}")
        # print out the grand total for all services
        print(f"Grand Total: ${self.amount_due:.2f}")

    # def available_spaces(self):
    #     """
    #     enhancement 2:
    #     Returns the dictionary of available spaces for all pet types
    #     """
    #     return {pet_type: info['available']
    #             for pet_type, info in self.SPACES.items()}

    def check_out(self):
        """
        Handles the pet check-out process

        Enhancement 3:
        updated to ask for the owners email address first to show the pets currently checked in (if any)
        and then allows them to choose which pet they would like to check-out. The owners email is asked
        for because during the check-in process, the owners email is tied to the specific pet they are
        checking in. Tying the owners email to the pet during check-in prevents mixing up data and checking
        out a dog with the same name.
        """
        while True:
            print("Please enter owner's email address: ")
            owner_email = input().strip()

            # ensure a valid email address is entered
            if '@' not in owner_email or '.' not in owner_email:
                print("Please enter a valid email address.")
                continue

            # find all active pets for this owner
            active_pets = self.db.find_pet_by_owner(owner_email)

            if not active_pets:
                print("No pets currently checked in under this email address.")
                return False

            # display all active pets for the owner
            print("\nCurrently checked in pets:")
            # give each pet entry its own number
            for i, pet in enumerate(active_pets, 1):
                print(f"{i}. {pet['name']} ({pet['type']})")
                if pet['type'] == 'dog':
                    print(f"   Weight: {pet['weight']} lbs")
                print(f"   Check-in date: {pet['check_in_date'].strftime('%Y-%m-%d %H:%M')}")

            # let owner select which pet to check out
            while True:
                try:
                    print("\nEnter the number of the pet you want to check out (or 0 to cancel): ")
                    selection = int(input())

                    if selection == 0:
                        return False

                    if 1 <= selection <= len(active_pets):
                        selected_pet = active_pets[selection - 1]
                        if self.db.pet_check_out(selected_pet['name'], owner_email):
                            print(f"Thank you for trusting us to watch after {selected_pet['name']}!")
                            print("We would love to see them again. Have a great day!")
                            self._reset_pet()
                            return True
                        else:
                            print("Checkout failed")
                            return False
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
                break
        return False

    def _reset_pet(self):
        """
        Returns all pet parameters to their default after check-out
        """
        self.pet_name = ""
        self.pet_type = ""
        self.pet_age = 0
        self.days_stay = 0
        self.amount_due = 0
        self.dog_weight = 0
        self.grooming_service = False
        self.daily_rate = 0
        self.grooming_fee = 0
        self.dog_size_category = None

    def pet_history(self, pet_name):
        """
        Enhancement 3:
        added to check for previous visits by the same pet
        """
        print("Please provide your email to view pet history: ")
        owner_email = input().strip()

        if '@' not in owner_email or '.' not in owner_email:
            print("Please enter a valid email address.")
            return None

        return self.db.pet_history(pet_name, owner_email)

def main():
    """
    This is the main function for the program, it allows for the program to be used and for the
    user to choose what they would like to do with the system. The customer can choose to check-in
    a pet, check-out a pet, view all available spaces, or exit the application.

    Enhancement 3:
    adds the option to view pet history from the database if previous data exists
    """
    # welcome the customer and create a new pet instance
    print("Welcome to the Pet Boarding System")
    main_menu = Pet()

    while True:
        print("Please select a menu option: ")
        print("1. Check-in a pet")
        print("2. Check-out a pet")
        print("3. View available spaces")
        print("4. View pet History")
        print("5. Exit")

        menu_selection = input()

        if menu_selection == "1":
            main_menu.check_in()

        elif menu_selection == "2":
            main_menu.check_out()

        elif menu_selection == "3":
            # checks for available spaces by getting information from database
            spaces = main_menu.db.get_available_space()
            print("Here are the spaces available: ")
            for pet_type, count in spaces.items():
                print(f"{pet_type.capitalize()}: {count}")

        elif menu_selection == "4":
            # shows pet history for the pet_name entered if data exists
            print("Enter the name of your pet to view boarding history: ")
            pet_name = input()
            history = main_menu.pet_history(pet_name)
            if history:
                print(f"Boarding history for {pet_name}: ")
                for record in history:
                    print(f"Check-in date: {record['check_in_date']}")
                    print(f"Days stay: {record['days_stay']}")
                    print(f"Amount due: ${record['amount_due']:.2f}")
                    print(f"Status: {record['status']}")
            else:
                print("No history for this pet.")

        elif menu_selection == "5":
            print("Thank you for using the Pet Boarding System")
            break

        else:
            print("Invalid entry, please enter a valid option")

if __name__ == "__main__":
    main()
```
## Database Program (MongoDB Integration)
```
"""
Author: Rob Crowe
Email: robert.crowe@snhu.edu
Class: CS-499 Capstone
Purpose: Capstone Project Enhancement 3 - Databases

Title: Pet Boarding Program

This program implements a MongoDB database system for the pet boarding application I am working on for
my capstone project. It handles all database operations like storing pet information, boarding records,
tracking available space, and customer data.
"""

from pymongo import MongoClient # import pymongo for use with MongoDB databases
import datetime # import for date and time information
import uuid # provides immutable UUID objects

class PetDatabase:
    """
    Handles all database operations for the mongodb database for the pet boarding application. Each pet
    is given a unique identifier and is linked to their owners information when the pet is checked-in.
    this function also tracks both active and historical boarding records.
    """

    def __init__(self):
        """
        Initializes the database connection and sets up required collections and indexes
        """
        try:
            # connect to mongodb database
            self.client = MongoClient('mongodb://localhost:27017/')

            # initialize database
            self.db = self.client['pet_boarding']

            # initialize database collections
            self.pets = self.db.pets
            self.boarding_records = self.db.boarding_records
            self.spaces = self.db.spaces

            # create indexes for database queries
            self.pets.create_index([('name', 1), ('owner_info.email', 1)], unique=True)
            self.boarding_records.create_index('pet_id')
            self.boarding_records.create_index([('status', 1), ('owner_info.email', 1)])

            # initialize spaces available
            if self.spaces.count_documents({}) == 0:
                self._initialize_spaces()

        # exception for if the database connection fails
        except Exception as e:
            print(f"Database Initialization error: {e}")
            raise

    def _initialize_spaces(self):
        """
        Initializes space allocation for space tracking
        """
        try:
            # create space data
            space_data = {
                'cat': {'total': 12, 'available': 12}, # 12 total cat spaces
                'dog': {'total': 30, 'available': 30}  # 30 total dog spaces
            }
            self.spaces.insert_one(space_data)
        except Exception as e:
            print(f"Space initialization error: {e}")
            raise

    def save_pet_checkin(self, pet_data, owner_info):
        """
        Save or update pet information during check-in and creates a new boarding record
        """

        try:
            # creates pet information for the database
            pet_info = {
                'name': pet_data.pet_name,
                'type': pet_data.pet_type,
                'age': pet_data.pet_age,
                'weight': pet_data.dog_weight if pet_data.pet_type == 'dog' else None,
                'owner_info': owner_info,
                'unique_id': str(uuid.uuid4()),
                'last_updated': datetime.datetime.now()
            }

            # try to find existing pet record
            existing_pet = self.pets.find_one({
                'name': pet_data.pet_name,
                'owner_info.email': owner_info['email']
            })

            if existing_pet:
                # update existing pet record
                self.pets.update_one(
                    {'_id': existing_pet['_id']},
                    {'$set': pet_info}
                )
                pet_id =existing_pet['_id']
            else:
                # create new pet record
                result = self.pets.insert_one(pet_info)
                pet_id = result.inserted_id

            # create an associated boarding record
            boarding_record = self.create_boarding_record(pet_data, pet_id)

            # update boarding record with owner information
            self.boarding_records.update_one(
                {'_id': boarding_record},
                {'$set': {'owner_info': owner_info}}
            )

            return pet_id

        except Exception as e:
            print(f"Error saving pet check-in: {e}")
            raise

    def find_pet_by_owner (self, owner_email):
        """
        Retrieves all active boarding records for pets linked to the owners email. Returns an empty
        pet list if there are no active records
        """

        try:
            # find all active boarding records for the owner
            active_records = self.boarding_records.find({
                'status': 'active',
                'owner_info.email': owner_email
            })

            # create an empty list for active pets
            active_pets = []
            # for all records in active records
            for record in active_records:
                # find pets linked to the owner
                pet = self.pets.find_one({'_id': record['pet_id']})
                # populate the list with all relevant information
                if pet:
                    pet_info = {
                        'name': pet['name'],
                        'type': pet['type'],
                        'weight': pet.get('weight'),
                        'check_in_date': record['check_in_date'],
                        'days_stay': record['days_stay'],
                        'amount_due': record['amount_due']
                    }
                    active_pets.append(pet_info)

            return active_pets

        except Exception as e:
            print(f"Error finding active pets: {e}")
            return

    def create_boarding_record(self, pet_data, pet_id):
        """
        Creates a new boarding record for the pets stay
        """

        try:
            # create boarding information
            boarding_info = {
                'pet_id': pet_id,
                'check_in_date': datetime.datetime.now(),
                'days_stay': pet_data.days_stay,
                'daily_rate': pet_data.daily_rate,
                'grooming_service': pet_data.grooming_service if pet_data.pet_type == 'dog' else False,
                'grooming_fee': pet_data.grooming_fee if pet_data.pet_type == 'dog' else 0,
                'amount_due': pet_data.amount_due,
                'status': 'active'
            }

            # insert boarding record into database and return its ID
            result = self.boarding_records.insert_one(boarding_info)
            return result.inserted_id

        except Exception as e:
            print(f"Error creating boarding record: {e}")
            raise

    def update_pet_record(self, pet_name, update_data):
        """
        Updates an existing pet record with new information
        """
        try:
            # update pet with new information
            self.pets.update_one(
                {'name': pet_name},
                {'$set': update_data} # update only specified fields
            )
        except Exception as e:
            print(f"Error updating pet record: {e}")
            raise

    def update_spaces(self, pet_type, checking_in=True):
        """
        Update the available spaces during pet check-in and check-out
        """

        try:
            # calculate based on check-in or check-out
            update_operation = {'$inc': {f'{pet_type}.available': -1 if checking_in else 1}}
            # update space count in database
            self.spaces.update_one({}, update_operation)

        except Exception as e:
            print(f"Error updating spaces: {e}")
            raise

    def get_available_space(self):
        """
        Retrieve current available space for both cats and dogs
        """

        try:
            # get current space information
            space_info = self.spaces.find_one()
            # return default values if no space exists
            if not space_info:
                return {'cat': 0, 'dog': 0}

            return {
                # return a dictionary of available spaces
                'cat': space_info['cat']['available'],
                'dog': space_info['dog']['available']
            }

        except Exception as e:
            print(f"Error getting available space: {e}")
            return {'cat': 0, 'dog': 0}

    def pet_check_out(self, pet_name, owner_email):
        """
        Processes a pet checking out, update boarding record status, update available spaces
        """

        try:
            # verify pet belongs to owner
            pet = self.pets.find_one({
                'name': pet_name,
                'owner_info.email': owner_email
            })
            if not pet:
                print("Pet not found or owner email does not match records")
                return False

            # find active boarding record for this pet
            active_record = self.boarding_records.find_one({
                'pet_id': pet['_id'],
                'status': 'active'
            })

            if not active_record:
                print("No active boarding record for this pet")
                return False

            # update boarding record status
            self.boarding_records.update_one(
                {'pet_id': pet['_id']},
                {'$set': {
                    'status': 'completed',
                    'check_out_date': datetime.datetime.now()
                }}
            )

            # update available spaces
            self.update_spaces(pet['type'], checking_in=False)
            return True

        except Exception as e:
            print(f"Error checking out pet: {e}")
            return False

    def pet_history(self, pet_name, owner_email):
        """
        Retrieve boarding history for a specific pet
        """

        try:
            # verify pet belongs to owner
            pet = self.pets.find_one({
                'name': pet_name,
                'owner_info.email': owner_email
            })
            if not pet:
                return None

            # get all boarding records for this pet
            cursor = self.boarding_records.find({'pet_id': pet['_id']})
            history = list(cursor)

            # add pet info to each record
            for record in history:
                record['pet_info'] = pet

            return history

        except Exception as e:
            print(f"Error retrieving pet history: {e}")
            return None

    def verify_pet_owner(self, pet_name, owner_email):
        """
        Verifies that a pet belongs to the correct owner
        """

        try:
            # verify pet belongs to owner
            pet = self.pets.find_one({
                'name': pet_name,
                'owner_info.email': owner_email
            })
            return pet is not None

        except Exception as e:
            print(f"Error verifying pet owner: {e}")
            return False

    def close_connection(self):
        """
        Close the database connection and clean up database resources
        """
        try:
            # close database connection
            self.client.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")
```
