from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from caffe2.python import core
from hypothesis import given
import caffe2.python.hypothesis_test_util as hu
import hypothesis.strategies as st
import numpy as np


class TestLossOps(hu.HypothesisTestCase):

    @given(n=st.integers(1, 8), **hu.gcs)
    def test_averaged_loss(self, n, gc, dc):
        X = np.random.rand(n).astype(np.float32)

        def avg_op(X):
            return [np.mean(X)]

        op = core.CreateOperator(
            "AveragedLoss",
            ["X"],
            ["y"],
        )

        self.assertReferenceChecks(
            device_option=gc,
            op=op,
            inputs=[X],
            reference=avg_op,
        )

        self.assertGradientChecks(
            device_option=gc,
            op=op,
            inputs=[X],
            outputs_to_check=0,
            outputs_with_grads=[0],
        )
