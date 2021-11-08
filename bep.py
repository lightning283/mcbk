import os,sys
from lib.mcbk import main as mc_main
if sys.argv[1] == "minecraft":
    if "upload" in  sys.argv:
        mc_main(sys.argv[2],upload=True)
    else:
        mc_main(sys.argv[2],upload=False)