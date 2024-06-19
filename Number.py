import phonenumbers
from phonenumbers import timezone, geocoder, carrier
import logging
import os

# Setting up logging
logging.basicConfig(filename='phonenumber_utility.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class PhoneNumberUtility:
    def __init__(self):
        self.numbers = []

    def validate_number(self, number):
        try:
            phone = phonenumbers.parse(number)
            if phonenumbers.is_valid_number(phone):
                return phone
            else:
                logging.error(f"Invalid number: {number}")
                print(f"Invalid number: {number}")
                return None
        except Exception as e:
            logging.error(f"Error parsing number {number}: {e}")
            print(f"Error parsing number {number}: {e}")
            return None

    def process_number(self, phone):
        try:
            time = timezone.time_zones_for_number(phone)
            car = carrier.name_for_number(phone, "en")
            reg = geocoder.description_for_number(phone, "en")

            result = {
                'number': phone,
                'time_zones': time,
                'carrier': car,
                'region': reg
            }
            return result
        except Exception as e:
            logging.error(f"Error processing number {phone}: {e}")
            print(f"Error processing number {phone}: {e}")
            return None

    def input_number(self):
        number = input("Enter Your Number with country code (e.g., +91xxxxxxxxxx): ")
        phone = self.validate_number(number)
        if phone:
            result = self.process_number(phone)
            if result:
                self.display_result(result)
                self.save_result(result)
                self.numbers.append(result)

    def batch_process(self, file_path):
        if not os.path.exists(file_path):
            logging.error(f"File not found: {file_path}")
            print(f"File not found: {file_path}")
            return

        with open(file_path, 'r') as file:
            for line in file:
                number = line.strip()
                phone = self.validate_number(number)
                if phone:
                    result = self.process_number(phone)
                    if result:
                        self.display_result(result)
                        self.save_result(result)
                        self.numbers.append(result)

    def display_result(self, result):
        print(f"Phone Number: {result['number']}")
        print(f"Time Zones: {result['time_zones']}")
        print(f"Carrier: {result['carrier']}")
        print(f"Region: {result['region']}\n")

    def save_result(self, result):
        with open('phonenumber_results.txt', 'a') as file:
            file.write(f"Phone Number: {result['number']}\n")
            file.write(f"Time Zones: {result['time_zones']}\n")
            file.write(f"Carrier: {result['carrier']}\n")
            file.write(f"Region: {result['region']}\n\n")
        logging.info(f"Saved result for number: {result['number']}")

    def display_menu(self):
        print("Phone Number Utility Menu")
        print("1. Process a single number")
        print("2. Batch process numbers from a file")
        print("3. Exit")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")
            if choice == '1':
                self.input_number()
            elif choice == '2':
                file_path = input("Enter the path to the file: ")
                self.batch_process(file_path)
            elif choice == '3':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    utility = PhoneNumberUtility()
    utility.run()
