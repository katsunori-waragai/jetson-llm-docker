## grounded-SAM docker
- docker environment for grounded SAM
https://github.com/IDEA-Research/Grounded-Segment-Anything


### status
sh docker_build.sh 
sh docker_run.sh
succeeded.

## usage
- download weight
- 
```
 python3 grounded_sam_demo.py   --config GroundingDINO/groundingdino/config/GroundingDINO_SwinT_OGC.py   --grounded_checkpoint groundingdino_swint_ogc.pth   --sam_checkpoint sam_vit_h_4b8939.pth   --input_image images/ego4d_2d386a76-9ef1-49ff-982e-d5e403bba456_12750.jpg   --output_dir "outputs"   --box_threshold 0.3   --text_threshold 0.25   --text_prompt "arm . door "   --device "cuda"
```

## todo
- use stable opencv-python


