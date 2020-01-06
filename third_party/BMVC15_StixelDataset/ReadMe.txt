A full list of Stixel bottom points is in the file StixelsGroundTruth.txt

Each line in the file represent a single point, in the following format:

series_date	series_id	frame_id	x	y	point_type(Train/Test)

In order to load and display Stixel bottom points on images, one needs to call:

DisplayStixels(gt_filename, kitti_base_dir)

Where gt_filename is full path file name for StixelsGroundTruth.txt, and kitti_base_dir is root directory to Kitti images databse.
In the code, it is assumed the Kitti images it kept in the following folder structure 
(as downloaded from Kitti site, the raw data section, synced+rectified sequences):

kitti_base_dir\2011_<series_date>\2011_<series_date>_drive_<series_id>_sync\image_02\data\<frame_id>.png
