import os
home_directory = os.environ['SSLKEYLOGFILE']
print(f"Home directory: {home_directory}")


with open("t.txt", "w") as file:
    file.write("hmm")
    
    
print(os.environ)