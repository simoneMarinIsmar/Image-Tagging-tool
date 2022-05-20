# Image-Tagging-tool

imageTagging.py is a very simple script for tagging relevant subjects into a set of images. It can be executed as command line and during the tagging operations the mouse can be used for selecting the relevant image regions. The commands for moving form one image to the next one, for saving a tagged image and for exiting are provided through the keyboard.
The script produces as output a text which each row contains the image file name, the image time stamp, the 8 verteices of the rotated bounding box containing a tagged relevant subject.

To execute the script can be executed through the following command line:

./imageTagging.py outFile outFileMode imageList indicesFile imgIndex

where:
- outFile: is the output file name containing the rotated bounding box information for all the tags.
- outFileMode: designated as “w” to overwrite the new outputs, or “a” to add new tags’ lines.
- imageList: for a text file composed by the date and path of the image.
- indicesFile: for a text file composed of integer numbers corresponding to each line of the imageList.
- imgIndex: for an integer number, between the numbers included in indicesFile, with the position where the operator wanted to start the tagging.

After the tagging of the relevant subject in one image, the operator could press “s” to save the tagged image, or “e” to escape from the executing code. Pressing "+" the output file is updated with the new tags and the next image can be processed.
If the tagged image and its outputs were saved, the code will ask the operator the species’ code for each tag operated."

Each row of the imageList file represents an image to be processed and has the following format:

image_date image_time image_full_path

....

image_date image_time image_full_path



Each row of the indicesFile file is a number representing the line number of the imageList file and has the following format:

number

...

number



Each row of the outFileMode represents a tagged region and has the following format:

image_full_path image_date image_time x1, y1, x2, y2, x3, y3, x4, y4 tag_label

...

image_full_path image_date image_time x1, y1, x2, y2, x3, y3, x4, y4 tag_label
