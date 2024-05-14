##
- mmsegmenation のライブラリは癖が強い。
- configファイルの影響を強く受けるようだ。
この記述は、img_file のdirname のdirname があることを前提としている。

```
Traceback (most recent call last):
  File "predict_capture.py", line 49, in <module>
    seg_result = inference_segmentor(model, cvimg)[0]
  File "/root/EgoHOS/mmsegmentation/mmseg/apis/inference.py", line 105, in inference_segmentor
    result = model(return_loss=False, rescale=True, **data)
  File "/usr/local/lib/python3.8/dist-packages/torch/nn/modules/module.py", line 1480, in _call_impl
    return forward_call(*args, **kwargs)
  File "/usr/local/lib/python3.8/dist-packages/mmcv/runner/fp16_utils.py", line 116, in new_func
    return old_func(*args, **kwargs)
  File "/root/EgoHOS/mmsegmentation/mmseg/models/segmentors/base.py", line 110, in forward
    return self.forward_test(img, img_metas, **kwargs)
  File "/root/EgoHOS/mmsegmentation/mmseg/models/segmentors/base.py", line 92, in forward_test
    return self.simple_test(imgs[0], img_metas[0], **kwargs)
  File "/root/EgoHOS/mmsegmentation/mmseg/models/segmentors/encoder_decoder.py", line 472, in simple_test
    seg_logit = self.inference(img, img_meta, rescale)
  File "/root/EgoHOS/mmsegmentation/mmseg/models/segmentors/encoder_decoder.py", line 457, in inference
    seg_logit = self.whole_inference(img, img_meta, rescale)
  File "/root/EgoHOS/mmsegmentation/mmseg/models/segmentors/encoder_decoder.py", line 419, in whole_inference
    seg_logit = self.encode_decode(img, img_meta)
  File "/root/EgoHOS/mmsegmentation/mmseg/models/segmentors/encoder_decoder.py", line 119, in encode_decode
    aux_path = os.path.join(os.path.dirname(os.path.dirname(img_file)), 'pred_twohands')
  File "/usr/lib/python3.8/posixpath.py", line 152, in dirname
    p = os.fspath(p)
TypeError: expected str, bytes or os.PathLike object, not NoneType
root@orin:~/EgoHOS/mmsegmentation# 
```

