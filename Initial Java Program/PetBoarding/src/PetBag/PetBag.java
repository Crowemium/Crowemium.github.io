package PetBag;

public class PetBag {
	
	public static void main(String[] args) {
		
		// main class for PetBoarding
		Pet newPet = new Pet("", "", 0, 0, 0, 0, 0);
		
		// call the pet check in function
		newPet.checkIn();
		
		// default constructor test
		//System.out.println("Pet Type" + newPet.getPetType());
		//System.out.println("Pet Name" + newPet.getPetName());
		//System.out.println("Pet Age" + newPet.getPetAge());
		//System.out.println("Dog Spaces Available" + newPet.getDogSpace());
		//System.out.println("Cat Spaces Available" + newPet.getCatSpace());
		//System.out.println("Days Stay" + newPet.getDaysStay());
		//System.out.println("Amount Due" + newPet.getAmountDue());
	}
}
