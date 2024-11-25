# docker for EgoHOS
- Arm detection and object detection in egcentric image
- There are 1st order and 2nd order objects.

## original repo
https://github.com/owenzlz/EgoHOS

## example of working result
![](doc/Egohos_example.png)

Segmentation for each left and right arm, hand and object.

## Procedure
```commandline
sh docker_build.sh
sh docker_run.sh

```
## Running in the Dockerfile
- Running a series of downloads.

## What we feel is missing from EGOHOS alone
- It doesn't include producing the position of the joints of the arms and hands.
- Nor is there a 3D version of it.
- So much so that it is not possible to make the hand work.
- 1st, 2nd order interacting object does not tell you what it is. 
- In the case of a hand handling an object, part of the hand is hidden.
  - It is important to predict the state of the hidden fingers.

```commandline
cd mmsegmentation # if you are not in this directory
sed -i 's/python /python3 /g' pred_all_obj1.sh
bash pred_all_obj1.sh

bash pred_all_obj2.sh

```

--mode two_hands_obj1 1st order interacting objects
--mode tow_hands_obj2 1st and 2nd order interacting objects
and.
When there is an action of pouring hot water from a pot to a pan, the pot is touching the hand, so the pot
1st order interacting object.
Correspondingly, there is a difference in the --checkpoint_file.


In predict_videos.py, which is called in predict_obj1_videos.sh, there is a part where the python interpreter is only described as python, which is also explicitly specified as python3.

The abbreviation “cb” is the contact boundary.
This allows us to know in which area the hand is in contact with the object.

### output 
testimages
testimages/images
testimages/pred_cb
testimages/pred_cb_vis
testimages/pred_obj1
testimages/pred_obj1_vis
testimages/pred_obj2
testimages/pred_obj2_vis
testimages/pred_twohands
testimages/pred_twohands_vis

## Reasoning with videos
- Video supports mp4 file format.
  - Files such as webm should be converted to mp4 in advance.
