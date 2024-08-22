from cryptography.fernet import Fernet

def authenticate_voter(voter_id, voter_list):
    if voter_id in voter_list:
        return True
    else:
        return False

def generate_key():
    return Fernet.generate_key()

def encrypt_vote(vote, key):
    fernet = Fernet(key)
    encrypted_vote = fernet.encrypt(vote.encode())
    return encrypted_vote

def store_vote(encrypted_vote, storage):
    storage.append(encrypted_vote)

def decrypt_vote(encrypted_vote, key):
    fernet = Fernet(key)
    decrypted_vote = fernet.decrypt(encrypted_vote).decode()
    return decrypted_vote

def tally_votes(storage, key):
    vote_count = {"Option1": 0, "Option2": 0}
    for encrypted_vote in storage:
        vote = decrypt_vote(encrypted_vote, key)
        if vote in vote_count:
            vote_count[vote] += 1
    
    print("Voting Results:")
    for option, count in vote_count.items():
        print(f"{option}: {count} votes")


voter_list = ["Voter1", "Voter2", "Voter3"]
storage = []
key = generate_key() 

while True:
    voter_id = input("Enter your Voter ID: ")
    if authenticate_voter(voter_id, voter_list):
        vote = input("Enter your vote (Option1/Option2): ")
        encrypted_vote = encrypt_vote(vote, key)
        store_vote(encrypted_vote, storage)
        print("Your vote has been cast successfully.")
        voter_list.remove(voter_id)
    else:
        print("Authentication failed.")
        
    continue_voting = input("Do you want to cast another vote or exit? (Type 'exit' to quit, anything else to continue): ").strip().lower()
    if continue_voting == 'exit':
        break

tally_votes(storage, key)
