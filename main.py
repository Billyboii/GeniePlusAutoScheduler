from autoscheduler.auth import get_session, get_theme_park
import json
import mousetools
import os

class textcolors:
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def display_rides(rides, selections, sorted_order):
    for idx, ride_id in enumerate(sorted_order):
        ride_details = rides[ride_id]
        selected = '[x]' if ride_id in selections else '[ ]'
        if selected == '[x]':
            print(textcolors.GREEN + f"{selected} {idx + 1}: {ride_details['name']}" + textcolors.ENDC)
        else:
            print(f"{selected} {idx + 1}: {ride_details['name']}")

def toggle_selection(ride_number, sorted_order, selections):
    if 0 < ride_number <= len(sorted_order):
        ride_id = sorted_order[ride_number - 1]
        if ride_id in selections:
            del selections[ride_id]
        else:
            selections[ride_id] = True
    else:
        print(textcolors.FAIL + "Invalid selection. Please enter a number within the range of available rides." + textcolors.ENDC)

def toggle_all_selections(sorted_order, selections):
    if len(selections) == len(sorted_order):
        selections.clear()  # Clear selections if all rides are already selected
    else:
        for ride_id in sorted_order:
            selections[ride_id] = True  # Select all rides

# assign priroty to rides based on user input
def assign_priority(selections, rides):
    priority = {}
    for ride_id in selections:
        priority[ride_id] = input(f"Enter priority for {rides[ride_id]['name']}: ")
    return priority

def mousetools_park():

    # Initialize the park object (example: Magic Kingdom)
    mk = mousetools.Park(80007944)

    # Fetch detailed wait times
    rides = mk.get_wait_times_detailed()

    selections = {}
    user_input = None

    # Sort rides and create a sorted order list
    sorted_order = [ride_id for ride_id, _ in sorted(rides.items(), key=lambda x: x[1]['name'])]

    # Main loop
    while user_input != 'n':
        clear_screen()
        display_rides(rides, selections, sorted_order)
        user_input = input("Enter a ride number to toggle selection, 'a' to toggle all, 'n' to proceed: ")

        if user_input.isdigit():
            ride_number = int(user_input)
            toggle_selection(ride_number, sorted_order, selections)
        elif user_input == 'a':
            toggle_all_selections(sorted_order, selections)

    # Assign priority to selected rides
    priority = assign_priority(selections, rides)

    # Sort rides based on priority
    sorted_order = [ride_id for ride_id, _ in sorted(priority.items(), key=lambda x: x[1])]
    clear_screen()

    # Output selected rides and their details
    for ride_id in sorted_order:
        try:
            ride_details = rides[ride_id]
            attraction = mousetools.Attraction(ride_id)
            name = ride_details['name']
            wait_time = attraction.get_wait_time()
            status = attraction.get_status()
            fastpass_available = attraction.fastpass_available()

            print(textcolors.BLUE + name + textcolors.ENDC +
                f" | Status: {textcolors.GREEN + status + textcolors.ENDC if status != 'Closed' else textcolors.FAIL + 'Closed' + textcolors.ENDC}" +
                f" | Wait time: {wait_time if wait_time is not None else 'N/A'}" +
                f" | FastPass Available: {textcolors.GREEN + 'Yes' if fastpass_available else textcolors.FAIL + 'No' + textcolors.ENDC}")
        except:
            print(textcolors.FAIL + f"Error fetching details for {ride_details['name']}" + textcolors.ENDC)

if __name__ == "__main__":
    session = get_session()
    print(json.dumps(get_theme_park(session, 80007944), indent=1))