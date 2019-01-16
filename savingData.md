# Saving Data from the GLP2ce ("the tester")

## Acceptable USB Storage
The tester requires that the target USB storage ("USB drive") have these characteristics:
1. The first partition on the USB drive needs to be a FAT16 partition. Only the first
   partition is seen by the tester.
2. The first partition needs to be 2GB or smaller, which is a limitation of FAT16.  I am
   unsure about the exact upper that is recognized by the tester, so the safest thing to
   do is to make this partition a bit smaller than 2 GB or smaller (e.g. <= 1.9GB).
3. Additional partitions of different formats may be made on the USB drive, but they won't
   be seen or usable by the tester.
4. The first partition needs to have a valid Microsoft Windows format on it.  The tester,
   I think, uses Microsoft Windows CE (probably why "ce" is in the model name). Generally,
   if you can read/write to the first partition from a Microsoft Windows computer, and the
   above requirements are met, then it should be usable in the tester.

## Saving Data Procedure
1. Insert a properly formatted USB drive in any port on the tester.
2. .... 

TODO 

## USB Drive Directory Structure
The tester creates the following directory structure ....
TODO 


