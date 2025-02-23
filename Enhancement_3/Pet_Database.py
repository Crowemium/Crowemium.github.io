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