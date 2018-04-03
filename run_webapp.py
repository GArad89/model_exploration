import os
import sys
from webapp import app


def main():
    app.run(host="0.0.0.0", port = 5001, debug=True)

if __name__=='__main__':
    main()

