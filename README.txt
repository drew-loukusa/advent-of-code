Wondering what to do?

Run generate_year.ps1

It will generate a new year directory, and then inside of that new year directory
it will generate 25 day directories. 

Inside each day, it will place 2 python scripts, 'part_a.py' and 'part_b.py'.

These are pre-configured to be able to pull down the puzzle input from the AOC website. 
If it breaks, then the dude in charge of AOC changed his website, or...

YOU NEED TO SET YOUR AOC_SESSION_TOKEN:

    1. Sign in to the AOC website
    2. Hit F12, go to Storage\Cookies, get your session cookie
    3. Place cookie in the AOC_SESSION_TOKEN.ps1 
    4. Activate your python env: `env\Scripts\Activate` 
        The Activate script is setup to run the session token script, so when you open a new terminal
        and activate the virtual environment, your token is set automatically.
        It it doesn't get set, you can run the scirpt yourself.