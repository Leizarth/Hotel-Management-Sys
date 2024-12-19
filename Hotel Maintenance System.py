### Hotel Maintenance System ###

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
        self.appliances = [] # Empty list of appliances
        self.add_standard_appliances() # method to add standard appliances

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



class MaintenanceOverviewSystem:
    def __init__(self, rooms):
        # Initialize with a list of rooms
        self.rooms = rooms
        self.fixed_appliances = 0 # Track the number of fixed appliances
        self.unfixed_appliances = 0 # Track the number of unfixed appliances
        self.fixed_rooms = []  # List of rooms with all appliances fixed
        self.unfixed_rooms = []  # List of rooms where some appliances couldn't be fixed
        self.skipped_rooms = []  # List of rooms skipped due to critical issues
        self.out_of_order_rooms = []  # Rooms marked as Out of Order
        self.out_of_service_rooms = []  # Rooms marked as Out of Service

    def add_fixed_room(self, room):
        # Add a room to the fixed list
        if room.room_number not in self.fixed_rooms:
            self.fixed_rooms.append(room.room_number)

    def add_unfixed_room(self, room):
        # Add a room to the unfixed list
        if room.room_number not in self.unfixed_rooms:
            self.unfixed_rooms.append(room.room_number)

    def add_skipped_room(self, room, status):
        # Add a room to the skipped list and track its status
        if room.room_number not in self.skipped_rooms:
            self.skipped_rooms.append(room.room_number)
            if status == "Out of Order":
                self.out_of_order_rooms.append(room.room_number)
            elif status == "Out of Service":
                self.out_of_service_rooms.append(room.room_number)

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
            # Sort by occupancy (occupied first) and then by room number
            sorted_rooms = sorted(rooms_with_issues, key=lambda x: (not x["occupied"], x["room_number"]))
            return sorted_rooms
        except Exception as e:
            print(f"Error retrieving rooms with issues: {e}")
            return []

    def generate_report(self):
        # Generate a detailed maintenance report
        try:
            print("\n--- Maintenance Report ---")
            print(f"Fixed Appliances: {self.fixed_appliances}")
            print(f"Unfixed Appliances: {self.unfixed_appliances}")
            print(f"Fixed Rooms: {len(self.fixed_rooms)} ({', '.join(self.fixed_rooms)})\n")
            print(f"Number of Unfixed Rooms left for tomorrow: {len(self.unfixed_rooms)} ({', '.join(self.unfixed_rooms)})")
            print(f"Skipped Rooms: {len(self.skipped_rooms)} ({', '.join(self.skipped_rooms)})")
            print(f"Out of Order Rooms: {len(self.out_of_order_rooms)} ({', '.join(self.out_of_order_rooms)})")
            print(f"Out of Service Rooms: {len(self.out_of_service_rooms)} ({', '.join(self.out_of_service_rooms)})")
            print(f"Remaining Rooms with Issues: {self.get_remaining_rooms_count()}")
            print("--------------------------")
        except Exception as e:
            print(f"Error generating report: {e}")

    def get_remaining_rooms_count(self):
        # Return the count of rooms still needing maintenance
        try:
            rooms_with_issues = self.get_rooms_with_issues()
            return len(rooms_with_issues)
        except Exception as e:
            print(f"Error counting remaining rooms: {e}")
            return 0



class Maintenance:
    def __init__(self, location="Maintenance's Office"):
        # Initialize with a starting location, defaulting to "Maintenance's Office"
        self.location = location

    def go_to_room(self, room_number):
        # Change the maintenance worker's location to the specified room
        try:
            self.location = room_number
            print(f"- Maintenance is going to Room {room_number}.")
        except Exception as e:
            print(f"Error moving to room: {e}")

    def fix_room(self, room, overview_system):
        try:
            # Check if the room has already been skipped
            if room.room_number in overview_system.skipped_rooms:
                print(f"Skipping Room {room.room_number} as it was already attempted and not fixable.")
                return

            # Check for broken appliances
            broken_appliances = room.check_appliances()
            if not broken_appliances:
                print(f"No issues found in Room {room.room_number}. Nothing to fix.")
                return

            all_fixed = True  # Track if all appliances in the room were fixed
            for appliance in broken_appliances:
                if random.random() < 0.1:  # 10% chance the appliance cannot be fixed 
                    print(f"Could not fix {appliance.name} in Room {room.room_number}.") 
                    all_fixed = False # this is set to false if any appliance cannot be fixed
                    overview_system.unfixed_appliances += 1 # increment the count of unfixed appliances
                    
                    # Check if the appliance is critical or non-critical 
                    if appliance.name in ["Air Conditioner", "Television"]:  
                        print(f"Marking Room {room.room_number} as Out of Order.") 
                        room.status = "Out of Order" # Room cannot be used
                        overview_system.add_skipped_room(room, "Out of Order")
                        return
                    else:  # Non-critical appliances
                        print(f"Marking Room {room.room_number} as Out of Service.")
                        room.status = "Out of Service" # Room can be used with limitations
                        overview_system.add_skipped_room(room, "Out of Service")
                        return
                else:
                    appliance.mark_as_functional()  # Appliance fixed successfully
                    print(f"Fixed {appliance.name} in Room {room.room_number}.")
                    overview_system.fixed_appliances += 1 # increment the count of fixed appliances

            if all_fixed: # checks if all appliances in the room were fixed
                room.update_status()
                overview_system.add_fixed_room(room)
            else:
                overview_system.add_unfixed_room(room)
        except Exception as e:
            print(f"Error fixing Room {room.room_number}: {e}")



#Main logic
if __name__ == "__main__":
    # Step 1: Create rooms
    random.seed(42)  # Random seed used for reproducibility
    rooms = []  # Empty list of rooms
    for i in range(1, 253):  # 253 rooms are created
        room_number = f"{i:03}"  # The rooms have 3-digit numbers assigned to them
        room_type = "standard" if i <= 20 else "suite"  # Ensures 20 standard rooms and 14 suites
        occupied = random.choice([True, False])  # Randomly assign occupancy
        room = Room(room_number, occupied) if room_type == "standard" else Suite(room_number, occupied) # Create a room object based on type
        rooms.append(room) # Add the room to the list

    print(f"Total rooms created: {len(rooms)}")
    print(f"Total number of occupied rooms: {len([room for room in rooms if room.occupied])}")
    print(f"Total number of vacant rooms: {len([room for room in rooms if not room.occupied])}")

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
    print("\nStarting maintenance workflow.\n")

    while True:
        # Get rooms with issues, excluding skipped rooms
        rooms_with_issues = [
            room_info for room_info in overview_system.get_rooms_with_issues()
            if room_info["room_number"] not in overview_system.skipped_rooms
        ]

        if not rooms_with_issues:
            print("No more rooms with unresolved issues. Ending workflow.")
            break

        # Goes to the next room with issues and fixes it based on the priority
        next_room_info = rooms_with_issues[0]
        next_room = next((room for room in rooms if room.room_number == next_room_info["room_number"]), None)
        
        if next_room:
            maintenance_worker.go_to_room(next_room.room_number)
            maintenance_worker.fix_room(next_room, overview_system)
        else:
            print("Error: Room with issues not found in the system.")

    # Step 6: Generate the maintenance report
    overview_system.generate_report()
