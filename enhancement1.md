[Home](README.md) -- [Code Review](CodeReview.md) -- [Enhancement One](enhancement1.md) -- [Enhancement Two](enhancement2.md) -- [Enhancement Three](enhancement3.md)

# Narrative
<p>For the first enhancement artifact, I chose a program from when I took IT-145 Foundation in Application Development where we created a pet boarding program, in Java, that tracked the number of pet spaces available, how many days the pet would stay, and if the pet owner wanted their pets groomed. We created pseudocode for a pricing calculator but never created the code for it, as that was not the point of the assignment. The reason I have included this artifact is that I wanted to have a baseline starter for my capstone project so that I could have a more solid plan for demonstrating my skills rather than jumping around to different projects from the past. For enhancement one specifically, I decided to convert the original Java program to the Python language so that I could demonstrate that I understand programming logic enough to translate from one language to another.</p> 

<p>The course outcomes I planned to meet with this enhancement were to show that I have the skills to translate a program from Java to Python to achieve the same functionality. However, I went slightly beyond that and included some other minor enhancements to improve the functionality, such as handling cat and dog check-ins separately, handling new and returning cats and dogs separately, and moving the grooming function (to be fully implemented later) to its own function as well.</p> 

<p>These enhancements create a cleaner program overall because it has specific functions instead of everything being contained within one function like in the Java program. I have also included much-needed improvements in the use of comments to explain what each function is supposed to do and used in-line comments as further explanations for what a line does within a function. I didn’t have many issues come up while converting the code because the program itself was simple to begin with, however, I do anticipate issues to crop up when performing my other planned enhancements to this program.</p> 

# Initial Java Program

### Pet Class
Link to [Pet.java](https://github.com/Crowemium/Crowemium.github.io/blob/main/Initial%20Java%20Program/PetBoarding/src/PetBag/Pet.java)

### Main Function
Link to [PetBag.java](https://github.com/Crowemium/Crowemium.github.io/blob/main/Initial%20Java%20Program/PetBoarding/src/PetBag/PetBag.java)

# Converted Python Program
```
"""
Author: Rob Crowe
Email: robert.crowe@snhu.edu
Class: CS-499 Capstone
Purpose: Capstone Project Enhancement 1 - Java to Python Conversion

Title: Pet Boarding Program

This program implements a Pet boarding program that handles basic check-in processes for
both cats and dogs. The program also contains space tracking functionality, gathers basic
pet information, and the pets length of stay. I have also included some minor improvements
over the original java program for enhanced functionality and improved error handling.

This program is the beginning of my capstone project and will develop throughout my time
in the CS-499 course. Expect major changes and enhancements to this program's functionality
in the coming weeks.
"""


class Pet:
    """
    The Pet class represents a pet for the boarding program and handles all pet-related
    information for the check-in process such as space management and information for
    both cats and dogs
    """
    def __init__(self, pet_type="", pet_name="", pet_age=0, dog_space=0, cat_space=0, days_stay=0):
        """
        Initialize the pet instance with default values
        (petType=string, petName=string, petAge=int, dogSpace=int, catSpace=int, daysStay=int)
        """
        self.pet_type = pet_type
        self.pet_name = pet_name
        self.pet_age = pet_age
        self.dog_space = dog_space
        self.cat_space = cat_space
        self.days_stay = days_stay

    def check_in(self):
        """
        Handle the check-in process for a pet, determine space availability,
        and gather pet information
        """
        # initialize total spaces available for both cats(12) and dogs(30)
        self.cat_space = 12
        self.dog_space = 30

        # print welcome message
        print("Welcome, are you checking in a cat or dog?:")
        pet_type = input().lower() #set all input to lowercase for comparison

        # if pet_type is cat handle cat check-in
        if pet_type == "cat":
            self._cat_checkin()

        # else if pet_type is dog, handle dog check-in
        elif pet_type == "dog":
            self._dog_checkin()

        # else the input is NOT cat or dog, return to check_in
        else:
            print("Invalid input, Please enter 'cat' or 'dog'.")
            self.check_in()

    def _cat_checkin(self):
        """
        This function specifically handles the cat check in if the string for check in is cat
        This is an improvement over the Java program because the original program did not
        specifically pertain to checking in a cat, It just had a general check in process.
        """
        # if cat space is greater than or equal to one
        if self.cat_space >= 1:
            # display cat space available and ask if new or returning
            print("Cat space is available! ^._.^= ∫")
            print("Is your cat a new or returning visitor?")
            # create new variable cat_visitor
            cat_visitor = input().lower() # force input to lowercase for string comparison

            if cat_visitor == "new":
                print("Welcome new visitor!")
                print("We'll need to collect some information about our new fluffy friend!")
                self._new_cat_info() # added new function to take care of information separately
            elif cat_visitor == "returning":
                print("A pleasure to see you again!")
                print("Allow us to update the information on your cat")
                self._returning_cat_info() # added a new function to take care of returning cats separately
            else:
                # input handling for if cat_visitor string is NOT new or returning
                print("Invalid Input, Please enter 'new' or 'returning'")
                self._cat_checkin()

            # decrease the available cat spaces
            self.cat_space -=1

        # else there are no cat spaces available
        else:
            print("Sorry but there is no cat spaces available at the moment.")

    def _new_cat_info(self):
        """
        This function is an addition that was not included in the original java program
        and serves as a separate function to enter information for new cats instead of
        including information entry in the main check-in function. Making a separate
        information entry for new cats cleans up the main check-in function.
        """
        # collect information for the new cat visitor
        print("What is your cats name?: ")
        self.pet_name = input()
        print("How old is your cat?: ")
        self.pet_age = int(input()) # will only accept an integer as the input
        print("How many days will your cat be staying?: ")
        self.days_stay = int(input()) # will only accept an integer as the input
        print("Thank you for providing us with your cat's information.")

    def _returning_cat_info(self):
        """
        This function is another addition to help clean up the original code and will handle
        gathering updated information for a returning cat (Future update, not in current build).
        """
        # collect information for a returning cat
        print("How many days will your cat be staying?: ")
        self.days_stay = int(input()) # will only accept an integer as the input
        #self.update_pet() # function to be added later

    def _dog_checkin(self):
        """
        This is an addition similar to the cat check-in process except this function is
        specifically for checking in a dog if the pet type string equals dog
        """
        # if dog space is greater than or equal to 1
        if self.dog_space >= 1:
            print("Dog space is available! (❍ᴥ❍ʋ)")
            print("Is your dog a new or returning visitor?")
            dog_visitor = input().lower() # force input to lowercase for string comparison

            if dog_visitor == "new":
                print("We'll need to collect some information about our new furry friend!")
                self._new_dog_info()
            elif dog_visitor =="returning":
                print("It's a pleasure to see you again!")
                print("Allow us to update the information on your dog.")
                self._returning_dog_info()
            else:
                # input handling for if dog_visitor string is NOT new or returning
                print("Invalid Input, Please enter 'new' or 'returning'")
                self._dog_checkin()

            # decrease the available dog space
            self.dog_space -= 1

        # else there are no dog spaces available
        else:
            print("Sorry but there is no dog spaces available at the moment.")

    def _new_dog_info(self):
        """
        This function is another addition that was not included in the original java program
        and serves as a separate function to enter information for new dogs instead of including
        information entry in the main check-in function. Making a separate information entry for
        new dogs cleans up the main check-in function.
        """
        # collect information on the new dog visitor
        print("What is your dogs name?: ")
        self.pet_name = input()
        print("How old is your dog?: ")
        self.pet_age = int(input())
        print("How many days will your dog be staying?: ")
        self.days_stay = int(input())

        # check if eligible for grooming service
        self._grooming_eligible()
        print("Thank you for providing us with your dog's information.")

    def _returning_dog_info(self):
        """
        This function handles information for a returning dog (feature to be added later)
        """
        print("How many days will your dog be staying?: ")
        self.days_stay = int(input())
        self._grooming_eligible()
        # self.update_pet() # function to be added later

    def _grooming_eligible(self):
        """
        This function will handle checking to see if a dog is eligible for grooming services
        based on their days stay. Further functionality to be added later.
        """
        if self.days_stay >= 2:
            print("grooming services are available for your dog!")
        else:
            print("Grooming is not available for your dog.")

def main():
    """
    This is the main function for the program, it allows for the program to be used
    """
    # create a new pet
    new_pet = Pet()

    # begin the check-in process
    new_pet.check_in()

if __name__ == "__main__":
    main()
```
