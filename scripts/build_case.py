from pathlib import Path

def main():
    case_dir = Path("cases/case1")
    print(f"Case directory ready at: {case_dir.resolve()}")

if __name__ == "__main__":
    main()
