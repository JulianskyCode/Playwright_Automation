import random
import string

# Lists of sample first and last names
first_names = [
    "John", "Jane", "Alice", "Bob", "Charlie", "David", "Eve", "Frank", "Grace", "Hank",
    "Ivy", "Jack", "Kathy", "Leo", "Mona", "Nina", "Oscar", "Paul", "Quincy", "Rita"
]
last_names = [
    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor",
    "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin", "Thompson", "Garcia", "Martinez", "Robinson"
]

def generate_first_name():
    """Generate a random first name from the list."""
    return random.choice(first_names)

def generate_last_name():
    """Generate a random last name from the list."""
    return random.choice(last_names)

def generate_postcode():
    """Generate a random UK-style postcode (e.g., AB1 2CD)."""
    letters = string.ascii_uppercase
    part1 = ''.join(random.choice(letters) for _ in range(2))  # e.g., "AB"
    part2 = str(random.randint(0, 9))                        # e.g., "1"
    part3 = str(random.randint(0, 9))                        # e.g., "2"
    part4 = ''.join(random.choice(letters) for _ in range(2))  # e.g., "CD"
    return f"{part1}{part2} {part3}{part4}"                  # e.g., "AB1 2CD"

def random_choice(choices):
    return random.choice(choices)