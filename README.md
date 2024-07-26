# cnv-file-simplication

<img src="https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExM2VobzE2M2p0YnR1MGpqeHQ4dGttb3MzeWJqYThoeHJ0cWZwZzF0aCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/V6bb0SM5h2xcQ/giphy.webp" alt="GIF" width="500"/>

Download the .exe file to get the tool.

1. Choose the file you wish to simplify
2. Choose the simplication option you want
   * The drop n option will leave every nth row
   * The average n will average ever n rows and turn it into a single row (assuming it is in the same arm otherwise it will stop the average for the last at most n-1 samples in the arm)
   * n is the number of rows you wish to drop or average out.
   * By default the app rounds to 4 sig figs and gets rid of unnecessary columns.
3. Click run
4. The app will then ask you where you wish to save the new file.
5. The app has progress bar and will inform you when it is done. If it fails please open an issue or email me poundspb@rose-hulman.edu.

Packages requirements to change the source code:

`pip install pandas`
`pip install tkinder`
`pip install pyinstaller`

To edit the app. Go to the source code in `src/main.py` make an changes.

Whe completed with the editing inside the src file run 

`pyinstaller --onefile --windowed main.py`
