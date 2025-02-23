[Home](README.md) -- [Code Review](CodeReview.md) -- [Enhancement One](enhancement1.md) -- [Enhancement Two](enhancement2.md) -- [Enhancement Three](enhancement3.md)

# Narrative
<p>This artifact continues the work I did for Enhancement 1, where I converted an old Java program to the Python language. Enhancement two is included as one of the artifacts for my ePortfolio because I want to show that I understand the different stages of developing an application. Enhancement two demonstrates my understanding of data structures and algorithms by improving on the work done on enhancement one by including functionality for better space management, a pricing calculator, a check-out process, and dictionaries for both space and price lookup. The inclusion of dictionaries serves as lookup tables to enhance the performance and maintainability of the program and makes it easy to add, update, or modify services or categories without having to use multiple conditional statements which allows for all variables to be updated within a group in one section of the program. The pet check-in method has been updated to be a more sophisticated decision tree that handles different pet types and service options without having two separate check-in methods for cats or dogs. A pricing calculator algorithm was created as its own method that works with the dictionaries to pull data as needed and works with the method I created to print out a receipt. The receipt printing method shows all relevant stay information for the pet, lists the costs of all services, and gives the total cost to the customer. I used formatted strings to pull the relevant information from the functions where they are used.</p>

<p>I made key improvements to demonstrate that I met the course outcomes that I planned to meet. I was able to transform the hard-coded values from my original enhancements into flexible dictionary data structures. I created lookup systems for pricing and space management. And I created the check-out system which completes the main functionality features for this program. during the process of implementing enhancement two for my capstone project created a little bit more difficulty for me because the program started to become more complex. I had to re-learn how to create dictionaries and how to implement them properly. To simplify the program a little bit and make it more dynamic, I also had to figure out how to use formatted strings to pull information from different functions because if I hadn’t streamlined the application, It would have been a much more complicated program where I would have needed to hard code values which would have made it confusing.</p>

# Data Structures and Algorithms
```
"""
Author: Rob Crowe
Email: robert.crowe@snhu.edu
Class: CS-499 Capstone
Purpose: Capstone Project Enhancement 2 - Data Structures and Algorithms

Title: Pet Boarding Program

This program is the continuation of the Pet boarding program which I converted from
Java for enhancement 1 of my capstone project. The goal of enhancement 2 is to keep
the same functionality as the original program and add on much-needed data structures
to enhance the functionality of the program.

This enhancement aims to include functionality for better space management, a pricing calculator,
a check-out process, and dictionaries for space and price lookup. I have also decided to include
a printout of the receipt to ensure the functions work as intended. This enhancement also contains
the inclusion of a menu system that has four options to choose from: 1. check-in, 2. check-out,
3. view available spaces, and 4. Exit. The inclusion of a menu makes the program much more functional
than the previous enhancement.
"""


class Pet:
    """
    The Pet class represents a pet for the boarding program and handles all pet-related
    information for the check-in process such as space management and information for
    both cats and dogs and houses the dictionaries for space and pricing information.
    Adding dictionaries makes it easy to add, update, or modify services or categories.
    """

    # dictionaries for cat and dog spaces
    SPACES = {
        'cat': {'total': 12, 'available': 12},
        'dog': {'total': 30, 'available': 30}
    }

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
        using dictionaries means we can get rid of the dog and cat space default values
        because they have already been defined
        """
        self.pet_type = pet_type
        self.pet_name = pet_name
        self.pet_age = pet_age
        #self.dog_space = dog_space
        #self.cat_space = cat_space
        self.days_stay = days_stay
        # the following attributes have been included for enhancement 2
        self.amount_due = amount_due
        self.dog_weight = 0 # used to determine pricing
        self.grooming_service = False # set to false by default, tracks if grooming services requested
        self.daily_rate = 0 # stores the daily boarding rate
        self.grooming_fee = 0 # stores the grooming fee
        self.dog_size_category = None

    def check_in(self):
        """
        Handle the check-in process for a pet, determine space availability,
        and gather pet information

        enhancement 2 now incorporates weight collection for dogs and integrates the pricing
        function while removing the reliance on initializing cat and dog spaces and simplifies
        the code for the check-in process by calling the dictionaries
        """
        # initialize total spaces available for both cats(12) and dogs(30)
        #self.cat_space = 12
        #self.dog_space = 30

        while True:
            # print welcome message
            print("Welcome, are you checking in a cat or dog?:")
            pet_type = input().lower()  # set all input to lowercase for comparison

            if pet_type in self.SPACES:
                self.pet_type = pet_type
                if self.check_available_space(pet_type):
                    self._pet_checkin()
                else:
                    print(f"Sorry, there are no {pet_type} spaces available.")
                break
            else:
                print("Invalid input, Please enter 'cat' or 'dog'")

    def _pet_checkin(self):
        """
        This function handles the check in process for all pets based on type and will call to the
        appropriate functions, cat or dog, respectively.

        Thanks to the inclusion of dictionaries in enhancement 2 the separate check ins for cats
        and dogs can be combined into one pet checkin process.
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
        This function gathers information on new cats and has been updated for enhancement 2
        to incorporate the daily fee for boarding a cat, calculating the fees, printing
        the receipt, and updating the cat space count.
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

        # set cat pricing, calculate fees, update cat spaces, and print receipt
        self._set_pricing()
        self.calculate_fees()
        self.update_space_count('cat')
        self.print_receipt()

    def _returning_cat_info(self):
        """
        Updated for enhancement 2 to include the daily fee for boarding a cat, calculating the fees,
        printing the receipt, and updating the cat space count.
        """
        # collect information for a returning cat
        print("How many days will your cat be staying?: ")
        self.days_stay = int(input()) # will only accept an integer as the input
        #self.update_pet() # function to be added later

        # set cat pricing, calculate fees, update cat spaces, and print receipt
        self._set_pricing()
        self.calculate_fees()
        self.update_space_count('cat')
        self.print_receipt()

    def _new_dog_info(self):
        """
        This function gathers information on new dogs and has been updated for enhancement 2
        to incorporate the daily fee for boarding a dog, checking grooming eligibility,
        calculating the fees, and printing the receipt.
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

        # determine price, check if eligible for grooming service, calculate fees, update dog spaces, print receipt
        self._set_pricing()
        self._grooming_eligible()
        self.calculate_fees()
        self.update_space_count('dog')
        self.print_receipt()

    def _returning_dog_info(self):
        """
        This function handles information for a returning dog (feature to be added later)

        Gathers stay duration for a returning dog, checks grooming eligibility, calculates fees,
        and moves the calculation for tracking dog spaces
        """
        print("How many days will your dog be staying?: ")
        self.days_stay = int(input())

        print("Please confirm your dogs weight in pounds")
        self.dog_weight = float(input())
        # determine price, check if eligible for grooming service, calculate fees, update dog spaces, print receipt
        self._set_pricing()
        self._grooming_eligible()
        self.calculate_fees()
        self.update_space_count('dog')
        self.print_receipt()
        # self.update_pet() # function to be added later

    def _determine_dog_size(self):
        """
        enhancement 2:
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
        enhancement 2:
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

        enhancement 2:
        The grooming eligible function has been updated to ask if the customer wants grooming
        services
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

    def check_available_space(self, pet_type):
        """
        enhancement 2:
        Checks if there is currently available space for the pet_type entered by pulling
        information from the spaces dictionary
        """
        return self.SPACES[pet_type]['available'] > 0

    def update_space_count(self, pet_type, checking_in=True):
        """
        enhancement 2:
        Update the space count during check-in or check-out, the dictionary will update according
        to the check in (subtract 1 space) or check out (add 1 space back) process
        """
        if checking_in:
            self.SPACES[pet_type]['available'] -= 1
        else:
            self.SPACES[pet_type]['available'] += 1

    def calculate_fees(self):
        """
        Enhancement 2:
        Calculate the total fees based on length of stay and services chosen
        """
        # calculate boarding cost without additional service
        self.amount_due = self.daily_rate * self.days_stay

        # adding additional grooming fee if applicable
        if self.grooming_service:
            self.amount_due += self.grooming_fee

    def print_receipt(self):
        """
        enhancement 2:
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

    def available_spaces(self):
        """
        enhancement 2:
        Returns the dictionary of available spaces for all pet types
        """
        return {pet_type: info['available']
                for pet_type, info in self.SPACES.items()}

    def check_out(self):
        """
        enhancement 2:
        Handles the pet check-out process
        """
        print("Enter the name of the pet you want to check out: ")
        checkout_name = input()

        if self.pet_name and checkout_name.lower() == self.pet_name.lower():
            self.update_space_count(self.pet_type, checking_in=False)
            print(f"Thank you for trusting us to watch after {self.pet_name}!")
            print("We would love to see them again. Have a great day!")
            self._reset_pet()
            return True
        else:
            print("Pet not found")
            return False

    def _reset_pet(self):
        """
        enhancement 2:
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

def main():
    """
    This is the main function for the program, it allows for the program to be used

    enhancement 2:
    adds a main menu to the program so the customer can choose to check-in or check-out their
    pet, they can also choose to view how many spaces are available for all pets
    """
    # welcome the customer and create a new pet instance
    print("Welcome to the Pet Boarding System")
    main_menu = Pet()

    while True:
        print("Please select a menu option: ")
        print("1. Check-in a pet")
        print("2. Check-out a pet")
        print("3. View available spaces")
        print("4. Exit")

        menu_selection = input()

        if menu_selection == "1":
            main_menu.check_in()

        elif menu_selection == "2":
            main_menu.check_out()

        elif menu_selection == "3":
            spaces = main_menu.available_spaces()
            print("Here are the spaces available: ")
            for pet_type, count in spaces.items():
                print(f"{pet_type.capitalize()}: {count}")

        elif menu_selection == "4":
            print("Thank you for using the Pet Boarding System")
            break

        else:
            print("Invalid entry, please enter a valid option")

if __name__ == "__main__":
    main()
```
