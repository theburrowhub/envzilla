import argparse


def main(argv=None):
    """Entry point for envzilla CLI."""
    parser = argparse.ArgumentParser(description="envzilla CLI")
    parser.parse_args(argv)
    print("envzilla is ready!")

if __name__ == "__main__":
    main()
