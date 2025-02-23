package PetBag;

import java.util.Scanner;

public class Pet {
	// Private variables
			private String petType;
			private String petName;
			private int petAge;
			private int dogSpace;
			private int catSpace;
			private int daysStay;
			private double amountDue;
			private Scanner input;
			
	// Default Constructor
	public Pet(String petType, String petName, int petAge, int dogSpace, int catSpace, int daysStay, double amountDue) {
				this.setPetType(petType);
				this.petName = petName;
				this.petAge = petAge;
				this.dogSpace = dogSpace;
				this.catSpace = catSpace;
				this.daysStay = daysStay;
				this.amountDue = amountDue;
				this.input = new Scanner(System.in);
				}
	
	// Check In
	public void checkIn() {
		// Cat Space
		setCatSpace(12);
					
		// Dog Space
		setDogSpace(30);
					
		System.out.println("Welcome, are you checking in a dog or cat?:");
					
		// Input from Scanner
		String petType = input.nextLine();
					
		// Determine if customer is checking in a cat or dog
		if (petType.equals("cat")) {
			// Check if available cat space
			if (getCatSpace() >= 1) {
				System.out.println("Cat space is available! ^._.^= ∫");
				System.out.println("Is your cat a new or returning visitor?");
				// Check if cat is new or returning visitor
				String catVisitor = input.nextLine();
				if (catVisitor.equals("new")) {
					System.out.println("Welcome new visitor!");
					System.out.println("We'll need to collect some information about our new fluffy friend!");
					System.out.println("What is your cat's name?");
					String petName = input.nextLine();
					setPetName(petName);
					System.out.println("How old is your cat?");
					int petAge = input.nextInt();
					setPetAge(petAge);
								
					System.out.println("How many days will your cat be staying?");
					int daysStay = input.nextInt();
					// Set amount of days
					setDaysStay(daysStay);
								
					System.out.println("Thank you for providing us with your cat's information");
					// Decrease available Cat spaces by 1
					int currentCatSpace = getCatSpace();
					setCatSpace(currentCatSpace - 1);
					
				} else if (catVisitor.equals("returning")) {
					System.out.println("A pleasure to see you again!");
					System.out.println("Allow us to update the information on your cat.");
								
					System.out.println("How many days will your cat stay?");
					int daysStay = input.nextInt();
					// Set amount of days for returning cats
					setDaysStay(daysStay);
								
					// Decrease Available cat space by 1
					int currentCatSpace = getCatSpace();
					setCatSpace(currentCatSpace - 1);
					updatePet();
				}
			} else {
				System.out.println("Sorry but there is no cat spaces available at the moment.");
						
			}
		} else if(petType.equals("dog")) {
			// Check if Space is available for dog
			if (getDogSpace() >= 1) {
				System.out.println("Dog space is avalable! (❍ᴥ❍ʋ)");
				System.out.println("Is your dog a new or returning visitor?");
				System.out.println();
				// Check if dog is new or returning visitor
				String dogVisitor = input.nextLine();
				if (dogVisitor.equals("new")) {
					System.out.println("We'll need to collect some information about our new furry friend!");
					System.out.println("What is your dogs name?");
					System.out.println();
					String petName = input.nextLine();
					setPetName(petName);
					System.out.println("How old is your dog?");
					System.out.println();
					int petAge = input.nextInt();
					setPetAge(petAge);
								
					System.out.println("How many days will your dog be staying?");
					System.out.println();
					int daysStay = input.nextInt();
					// Set amount of days
					setDaysStay(daysStay);
								
					// Check if grooming services are needed
					if (daysStay >= 2) {
						System.out.println("Grooming services are available for your dog!");
					} else {
						System.out.println("Grooming is not available for your dog.");
					}
								
					System.out.println("Thank you for prividing us with your dog's information.");
								
					// Decrease available dog space by 1
					int currentDogSpace = getDogSpace();
					setDogSpace(currentDogSpace - 1);
							
				} else if (dogVisitor.equals("returning")) {
					System.out.println("It's a pleasure to see you again!");
					System.out.println("Allow us to update the information on your dog.");
								
					System.out.println("How many days will your dog be staying?");
					int daysStay = input.nextInt();
					setDaysStay(daysStay);
								
					// Check if grooming services are needed
					if(daysStay >= 2) {
						System.out.println("Grooming services are available for your dog!");
					} else {
						System.out.println("Grooming is not available for your dog.");
					}
								
					// Decrease available dog space by 1
					int currentDogSpace = getDogSpace();
					setDogSpace(currentDogSpace - 1);
					updatePet();
				}
			} else {
				System.out.println("Sorry but there is no dog spaces available at the moment.");
			}
					
		} else {
			System.out.println("Please enter 'cat' or 'dog'.");
			checkIn();
		}
	}
	
	public void cleanup() {
		if (input != null) {
			input.close();
		}
	}
	
	public String getPetType() {
		return petType;
	}

	public void setPetType(String petType) {
		this.petType = petType;
	}
				
	public String getPetName() {
		return petName;
	}
				
	public void setPetName(String petName) {
		this.petName = petName;
	}
				
	public int getPetAge() {
		return petAge;
	}
				
	public void setPetAge(int petAge) {
		this.petAge = petAge;
	}

	public int getDogSpace() {
		return dogSpace;
	}

	public void setDogSpace(int dogSpace) {
		this.dogSpace = dogSpace;
	}
				
	public int getCatSpace() {
		return catSpace;
	}

	public void setCatSpace(int catSpace) {
		this.catSpace = catSpace;
	}
				
	public int getDaysStay() {
		return daysStay;
	}
				
	public int setDaysStay(int daysStay) {
		return daysStay;
	}
				
	public double getAmountDue() {
		return amountDue;
	}
				
	public double setAmountDue(double amountDue) {
		return amountDue;
	}
	public void updatePet() {
		updatePet();
					
	}
}
