import hashlib
import logging
from datetime import datetime
import os
from tqdm import tqdm


# Set the log filename for storing the log messages
log_filename = "problem3/logger.log"

# Remove the log file if it already exists to start fresh
if os.path.exists(log_filename):
    os.remove(log_filename)

# Configure the logging settings, including the log file name and format
logging.basicConfig(filename=log_filename, level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S')
logger = logging.getLogger()
prefix_cache = {}


# Define the student ID
student_id = "111511157"

# Generate the SHA-256 hash of the student ID as the pre-image
preImage = hashlib.sha256(student_id.encode()).hexdigest()
logger.info(f"[preImage] {preImage}")

# Initialize the starting block number
start_block = 1

# Determine the starting block by comparing the pre-image with the student ID
for i in range(len(student_id)):
    if preImage[i] != student_id[i]:
        break
    start_block += 1

# Store the previous hash as the pre-image initially
previous_hash = preImage

# Set the maximum number of rounds and the nonce limit
max_round = 10
nonce_limit = 0xffffffff
round_num = start_block

# Loop through each round until the maximum round is reached
while round_num <= max_round:
    # Get the prefix from the student ID based on the current round number
    prefix = student_id[:round_num]

    print(f"Round {round_num}")
    print(f"Prefix: {prefix}")

    found = False
    # Loop through possible nonce values to find a valid hash
    for nonce in tqdm(range(nonce_limit + 1)):

        nonce_hex = f"{nonce:08x}"  # Format the nonce as a hexadecimal string
        block_input = previous_hash + nonce_hex  # Create the block input
        block_hash = hashlib.sha256(block_input.encode()).hexdigest()  # Compute the block hash

        # Check if the block hash starts with the current prefix
        if block_hash.startswith(prefix):
            logger.info(f"[Round {round_num} with nonce {nonce_hex}] {block_hash}")
            previous_hash = block_hash  # Update the previous hash
            found = True

            # Check if the current hash starts with the next prefix
            while round_num + 1 <= max_round and previous_hash.startswith(student_id[:round_num + 1]):
                round_num += 1
                logger.info(f"[Round {round_num} without nonce] {previous_hash}")
            break

    # If no valid hash was found after exhausting all nonces
    if not found:
        now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')  # Get the current timestamp
        with open(log_filename, "a") as f:
            f.write(f"{now} [EROR] [Round {round_num}] not found with running out of nonce\n")  # Log the error
        break

    round_num += 1  # Move to the next round number
