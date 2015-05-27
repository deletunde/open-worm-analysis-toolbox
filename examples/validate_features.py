# -*- coding: utf-8 -*-
"""
Validate that the features calculations in movement_validation
match those of the original Matlab codebase, by comparing
calculated features with a saved copy of the file generated by 
the original Matlab code.

To run this code files should be obtained from:
https://drive.google.com/folderview?id=0B7to9gBdZEyGNWtWUElWVzVxc0E&usp=sharing

In addition the user_config.py file should be created in the 
movement_validation package based on the user_config_example.txt

"""

import sys, os, time

# We must add .. to the path so that we can perform the 
# import of movement_validation while running this as 
# a top-level script (i.e. with __name__ = '__main__')
sys.path.append('..')
from movement_validation import user_config, NormalizedWorm
from movement_validation import WormFeatures, VideoInfo, config


def main():
    """
    Compare Schafer-generated features with our new code's generated features

    """
    # A better method after Python 3.3 is to use time.monotonic
    if sys.version_info[0] >= 3 and sys.version_info[1] >= 3:
        timer_function = time.monotonic
    else:
        timer_function = time.time

    start_time = timer_function()
    
    # Set up the necessary file paths for file loading
    #----------------------
    base_path = os.path.abspath(user_config.EXAMPLE_DATA_PATH)

    matlab_generated_file_path = os.path.join(
        base_path,'example_video_feature_file.mat')

    data_file_path = os.path.join(base_path,"example_video_norm_worm.mat")

    # OPENWORM
    #----------------------
    # Load the normalized worm from file
    nw = NormalizedWorm.from_schafer_file_factory(data_file_path)

    # The frame rate is somewhere in the video info. Ideally this would all
    # come from the video parser eventually
    vi = VideoInfo('Example Video File', config.FPS)

    # Generate the OpenWorm movement validation repo version of the features
    openworm_features = WormFeatures(nw, vi)

    # SCHAFER LAB
    #----------------------
    # Load the Matlab codes generated features from disk
    matlab_worm_features = WormFeatures.from_disk(matlab_generated_file_path)

    # COMPARISON
    #----------------------
    # Show the results of the comparison
    print("\nComparison of computed features to those computed with "
          "old Matlab code")

    print("Locomotion: " + 
        str(matlab_worm_features.locomotion == openworm_features.locomotion))

    print("Posture: " +
        str(matlab_worm_features.posture == openworm_features.posture))

    print("Morphology: " +
        str(matlab_worm_features.morphology == openworm_features.morphology))

    print("Path: " +
        str(matlab_worm_features.path == openworm_features.path))

    print("\nDone validating features")
    print("Time elapsed: %.2f seconds" % (timer_function() - start_time))


if __name__ == '__main__':
    main()
