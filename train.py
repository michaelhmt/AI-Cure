import sys
import os

if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(this_dir)

    import apps.run_holo_cure as run_holo_cure
    run_holo_cure.main()

