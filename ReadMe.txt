SweePy by Thomas O'Malley at the Illinois State Geological Survey is designed for the State Geothermal Data Project's ISGS 10.02 Geothermal Server.

SweePy is great at removing old data and projects from your service directory.  Don't clean up after yourself; let SweePy do it.

SweePy works by parsing ArcGIS Server's CFG files, and compiling a list of the MXD files referenced in them.  Each MXD file's required data sources are recorded.  SweePy then searches the service directory for all mdb, gdb, and mxd files and creates a list.  Necessary files (MXD files referenced in the CFG files, and their data sources) are then removed from this list, and what remains is a list of files that aren't vital to published services.  These files are then relocated and organized into a file tree by state name and file type.

SweePy incorporates both the Recursive_Glob and File_System_Restructure projects (found at https://github.com/Thom-OMalley)

*Not designed to work on all systems as-is.*