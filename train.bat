@echo off
echo "This will probably explode your computer"
echo "Are you sure you want to do this?"
echo "Press Ctrl C to cancel"
pause

for /L %%C in (550, 50, 600) DO (
    for /L %%D in (200, 50, 400) DO (
        echo "Training for DBP: 300, OPENING_DIST: 190, A: %%C, JUMP_V: %%D . . ."
        python train.py 300 190 %%C %%D 75
    )
)


for /L %%A in (350, 50, 400) DO (
    for /L %%B in (150, 40, 200) DO (
        for /L %%C in (300, 50, 600) DO (
            for /L %%D in (200, 50, 400) DO (
                echo "Training for DBP: %%A, OPENING_DIST: %%B, A: %%C, JUMP_V: %%D . . ."
                python train.py %%A %%B %%C %%D 75
            )
        )
    )
)
