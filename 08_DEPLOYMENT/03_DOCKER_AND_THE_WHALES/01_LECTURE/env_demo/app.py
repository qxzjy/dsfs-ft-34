import os

def main():
    print("Cakes are the best!")
    with open("favorites_cakes.txt") as f:
        print(f.read())
    print(f"And I like {os.environ['ENV_1']} and {os.environ['ENV_2']} too!")

if __name__ == "__main__":
    main()