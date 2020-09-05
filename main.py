import tkinter as tk

from frontend import MainApplication
from utils.log import logger

COPYRIGHT = r"""
   ______      _             ______     _ __  _            __
  / ____/___  (_)___  ____ _/ ____/____(_) /_(_)________ _/ /
 / / __/ __ \/ / __ \/ __ `/ /   / ___/ / __/ / ___/ __ `/ / 
/ /_/ / /_/ / / / / / /_/ / /___/ /  / / /_/ / /__/ /_/ / /  
\____/\____/_/_/ /_/\__, /\____/_/  /_/\__/_/\___/\__,_/_/   
                   /____/                                    

Copyright 2020 mixmoe, all rights reserved.
Publish under GPLv3 license
Repository: https://github.com/mixmoe/PyGoingCritical
///SCHOOL PROJECT DEMO, NOT OPENSOURCED YET///
"""  # noqa:W291

if __name__ == "__main__":
    logger.warning(COPYRIGHT)
    root = tk.Tk()
    root.wm_title("Influence Simulation")
    main = MainApplication(root)
    main.pack()
    root.mainloop()
