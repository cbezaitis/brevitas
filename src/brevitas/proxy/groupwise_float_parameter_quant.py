from typing import Any, Tuple

import torch.nn as nn

from brevitas.inject import BaseInjector as Injector
from brevitas.proxy.float_parameter_quant import WeightFloatQuantProxyFromInjectorBase
from brevitas.quant_tensor import GroupwiseFloatQuantTensor
from brevitas.utils.quant_utils import _CachedIOGroupwiseFloat


class GroupwiseWeightFloatQuantProxyFromInjector(WeightFloatQuantProxyFromInjectorBase):

    def __init__(self, quant_layer: nn.Module, quant_injector: Injector) -> None:
        super().__init__(quant_layer, quant_injector)
        self.cache_class = _CachedIOGroupwiseFloat

    @property
    def group_dim(self):
        return self.quant_injector.group_dim

    @property
    def group_size(self):
        return self.quant_injector.group_size

    def create_quant_tensor(self, qt_args: Tuple[Any]) -> GroupwiseFloatQuantTensor:
        out, scale, zero_point, exponent_bit_width, mantissa_bit_width, exponent_bias, saturating, inf_values, nan_values = qt_args
        return GroupwiseFloatQuantTensor(
            out,
            scale,
            zero_point,
            self.group_size,
            self.group_dim,
            exponent_bit_width,
            mantissa_bit_width,
            exponent_bias,
            saturating,
            inf_values,
            nan_values,
            self.is_signed,
            self.training)
