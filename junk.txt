root@waragai-orin:~/nanoowl# cd examples
root@waragai-orin:~/nanoowl/examples# python3 owl_predict.py \
>     --prompt="[an owl, a glove]" \
>     --threshold=0.1 \
>     --image_encoder_engine=../data/owl_image_encoder_patch32.engine
['an owl', ' a glove']
0.1
/usr/local/lib/python3.8/dist-packages/torch/storage.py:315: UserWarning: TypedStorage is deprecated. It will be removed in the future and UntypedStorage will be the only storage class. This should only matter to you if you are using storages directly.
  warnings.warn(message, UserWarning)
/usr/local/lib/python3.8/dist-packages/torch/functional.py:504: UserWarning: torch.meshgrid: in an upcoming release, it will be required to pass the indexing argument. (Triggered internally at /home/riship/old_pyt/pytorch/aten/src/ATen/native/TensorShape.cpp:3435.)
  return _VF.meshgrid(tensors, **kwargs)  # type: ignore[attr-defined]
/root/nanoowl/nanoowl/image_preprocessor.py:71: UserWarning: The given NumPy array is not writable, and PyTorch does not support non-writable tensors. This means writing to this tensor will result in undefined behavior. You may want to copy the array to protect its data or make it writable before converting it to a tensor. This type of warning will be suppressed for the rest of this program. (Triggered internally at /home/riship/old_pyt/pytorch/torch/csrc/utils/tensor_numpy.cpp:199.)
  image = torch.from_numpy(np.asarray(image))
root@waragai-orin:~/nanoowl/examples# 

