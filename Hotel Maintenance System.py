### Hotel Maintenance System

#installing random library if not already installed
!pip install random
# importing random library
import random

# Defining the Appliance class
class Appliance:
    def __init__(self, name, status):
        # Initialize the appliance with a name and status (Functional or Broken)
        self.name = name
        self.status = status

    def mark_as_broken(self):
        # Mark the appliance as broken
        self.status = "Broken"

    def mark_as_functional(self):
        # Mark the appliance as functional
        self.status = "Functional"

    def __str__(self):
        # Return a string representation of the appliance's status
        return f"{self.name}: {self.status}"
    

# Defining the Room class
class Room:
    def __init__(self, room_number, occupied=False):
        # Initialize the room with a room number, occupancy status, status, and an empty list of appliances
        
        self.room_number = room_number
        self.occupied = occupied
        self.status = "Usable"  # Default status is "Usable"
        self.appliances = []
        self.add_standard_appliances()

    def add_standard_appliances(self):
        # Add appliances specific to a standard room
        self.add_appliance("Mini Fridge")
        self.add_appliance("Air Conditioner")
        self.add_appliance("iPad")
        self.add_appliance("Television")

    def add_appliance(self, name, status="Functional"):
        # Add a new appliance to the room with a default status of "Functional"
        try:
            appliance = Appliance(name, status)
            self.appliances.append(appliance)
        except Exception as e:
            print(f"Error adding appliance: {e}")

    def check_appliances(self):
        # Check all appliances in the room and return a list of broken appliances
        try:
            broken_appliances = [appliance for appliance in self.appliances if appliance.status == "Broken"]
            return broken_appliances
        except Exception as e:
            print(f"Error checking appliances: {e}")
            return []

    def update_status(self):
        # Update the room's status based on appliance conditions
        broken_appliances = self.check_appliances()
        if any(appliance.name in ["Air Conditioner", "Television"] and appliance.status == "Broken" for appliance in broken_appliances):
            self.status = "Out of Order"  # Room cannot be used
        elif broken_appliances:
            self.status = "Out of Service"  # Room can be used with limitations
        else:
            self.status = "Usable"

    def __str__(self):
        # Return a string showing all appliances and their statuses
        appliance_status = "\n    ".join(str(appliance) for appliance in self.appliances)
        occupancy_status = "Occupied" if self.occupied else "Vacant"
        return f"Room {self.room_number} ({occupancy_status}, {self.status}) Appliances:\n    {appliance_status}"

# Defining the Suite class (inherits from Room Class)
class Suite(Room):
    def __init__(self, room_number, occupied=False):
        # Initialize the suite using the Room class's constructor
        super().__init__(room_number, occupied)
        self.add_suite_appliances()

    def add_suite_appliances(self):
        # Add additional appliances specific to suites
        self.add_appliance("Microwave")
        self.add_appliance("Jacuzzi")


# Define the MaintenanceOverviewSystem class
class MaintenanceOverviewSystem:
    def __init__(self, rooms):
        # Initialize with a list of rooms
        self.rooms = rooms

    def get_rooms_with_issues(self):
        # Return a sorted list of rooms with broken appliances, prioritizing occupied rooms 
        try:
            rooms_with_issues = [
                {
                    "room_number": room.room_number,
                    "occupied": room.occupied,
                    "broken_appliances": room.check_appliances()
                }
                for room in self.rooms if room.check_appliances()
            ]
            # Sort by occupancy (occupied first) and then by room number (sorting algorithm)
            sorted_rooms = sorted(rooms_with_issues, key=lambda x: (not x["occupied"], x["room_number"]))
            return sorted_rooms
        except Exception as e:
            print(f"Error retrieving rooms with issues: {e}")
            return []

    def get_remaining_rooms_count(self):
        # Return the count of rooms still needing maintenance
        try:
            rooms_with_issues = self.get_rooms_with_issues()
            return len(rooms_with_issues)
        except Exception as e:
            print(f"Error counting remaining rooms: {e}")
            return 0


# Define the Maintenance class
class Maintenance:
    def __init__(self, location="Office"):
        # Initialize with a starting location, defaulting to "Office"
        self.location = location
        self.fixed_appliances = 0
        self.unfixed_appliances = 0

    def go_to_room(self, room_number):
        # Change the maintenance worker's location to the specified room
        try:
            self.location = room_number
            print(f"- Maintenance is going to Room {room_number}.")
        except Exception as e:
            print(f"Error moving to room: {e}")

    def fix_room(self, room):
        # Fix all broken appliances in the specified room
        try:
            if not room.check_appliances(): # If there is no broken appliances, then does nothing and return an error message
                print(f"No issues found in Room {room.room_number}. Nothing to fix.")
                return
            for appliance in room.check_appliances():
                if random.random() < 0.1:  # 10% chance the appliance cannot be fixed
                    print(f"Could not fix {appliance.name} in Room {room.room_number}.")
                    self.unfixed_appliances += 1 # If the appliance cannot be fixed, then it is added to the list of unfixed appliances
                    if appliance.name in ["Air Conditioner", "Television"]: # If a critical appliance cannot be fixed, then the room is marked as "Out of Order"
                        print(f" Marking room {room.room_number} as Out of Order.")
                        room.status = "Out of Order" 
                        print(f"Room {room.room_number} status is now changed to OOO.")
                        return
                    else: # If a non-critical appliance cannot be fixed,then it marks the room as Out of Service
                        print(f"Marking room {room.room_number} as Out of Service.")
                        room.status = "Out of Service"
                        print(f"Room {room.room_number} status is now changed to Out of Service.")

                else:
                    appliance.mark_as_functional() # If the appliance can be fixed, then it is marked as functional
                    print(f"Fixed {appliance.name} in Room {room.room_number}.")
            room.update_status()
        except Exception as e:
            print(f"Error fixing room {room.room_number}: {e}") 

    def determine_next_room(self, rooms_with_issues):
        # Determine the next room to fix based on the sorted list of rooms with issues
        try:
            if not rooms_with_issues: # If there are no rooms with issues, then it returns "None"
                print("No rooms with issues to fix.")
                return None
            next_room = rooms_with_issues[0]["room_number"] # The next room to fix will be the first room in the list
            return next_room
        except Exception as e:
            print(f"Error determining next room: {e}")
            return None

    def log_location(self):
        # Print the current location of the maintenance worker
        try:
            print(f"Maintenance is currently at {self.location}.")
        except Exception as e:
            print(f"Error logging location: {e}")

    def generate_report(self):
        # Generate a final report of the rooms and the appliances that couldn't be fixed
        try:
            print("\nStarting maintenance report.")
            print(f"Could not fix {self.unfixed_appliances} appliances.") # Prints the number of appliances that couldn't be fixed
            print("\nMaintenance report completed.")
            self.fixed_appliances = 0 # Reset the count of fixed and unfixed appliances
        except Exception as e:
            print(f"Error generating report: {e}")


# Main Logic
if __name__ == "__main__":
    # Step 1: Create rooms
    random.seed(42)  # Random seed used for reproducibility
    rooms = [] # Empty list of rooms
    for i in range(1, 201): # 200 rooms are created
        room_number = f"{i:03}"  # the rooms have 3-digit numbers assigned to them
        room_type = "standard" if i <= 140 else "suite" # these makes sure that there are 20 standard rooms and 10 suites
        occupied = random.choice([True, False])  # Randomly assign occupancy
        room = Room(room_number, occupied) if room_type == "standard" else Suite(room_number, occupied)
        rooms.append(room) 

    print(f"Total rooms created: {len(rooms)}")
    print(f" Total number of occupied rooms: {len([room for room in rooms if room.occupied])}")
    print(f" Total number of vacant rooms: {len([room for room in rooms if not room.occupied])}")

    # Step 2: Randomly break appliances
    broken_count = 0
    for room in rooms:
        for appliance in room.appliances:
            if random.random() < 0.1:  # 10% chance to break
                appliance.mark_as_broken()
                broken_count += 1

    print(f"Total broken appliances: {broken_count}\n")

    # Step 3: Initialize MaintenanceOverviewSystem
    overview_system = MaintenanceOverviewSystem(rooms)

    # Step 4: Initialize Maintenance
    maintenance_worker = Maintenance()

    # Step 5: Maintenance workflow

    print("Starting maintenance workflow.\n")
    while True:
        rooms_with_issues = overview_system.get_rooms_with_issues()
        if not rooms_with_issues:
            break

        next_room_info = rooms_with_issues[0]  # Get highest priority room
        next_room = next((room for room in rooms if room.room_number == next_room_info["room_number"]), None)

        if next_room:
            maintenance_worker.go_to_room(next_room.room_number)
            maintenance_worker.fix_room(next_room)
        else:
            print("Error: Room with issues not found in the system.")

    # Step 6: Generate the maintenance report
    maintenance_worker.generate_report()
