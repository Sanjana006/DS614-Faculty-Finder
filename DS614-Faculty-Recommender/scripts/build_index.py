import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from recommender.index_builder import build_index

if __name__ == "__main__":
    build_index()
