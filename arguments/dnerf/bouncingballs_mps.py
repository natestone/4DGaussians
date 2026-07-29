# RaceColumn MPS densification config.
#
# _native.py converts the means2D gradient to NDC (x W/2, H/2) to match INRIA's
# convention (depth-diff-gaussian-rasterization backward.cu:460,545:
# dL_dmean2D = dL/d(delta) * 0.5*W); measured ~5x below INRIA's stat at p99, so
# the naive-principled threshold is ~2e-4/5 ~= 4e-5.
#
# BUT densification is a cliff on this scene, not a stable knob:
#   4e-5   -> runs away to ~310k points and diverges into floaters/chaos
#   1.5e-4 -> barely grows (~2.7k), reconstruction never forms
# There is no stable middle because the fit does not improve fast enough to
# taper the means2D gradient and self-limit densification the way reference
# 4DGaussians does. So the real remaining work is training *stability* (the
# deformation<->densification interaction, LR/schedule, floater pruning), not
# threshold tuning. The value below is a middle estimate to iterate from; it is
# NOT yet a validated setting. See 4dgs-metal-rasterizer docs/M3_ROADMAP.md M4.
_base_ = './bouncingballs.py'
OptimizationParams = dict(
    densify_grad_threshold_coarse = 8e-5,
    densify_grad_threshold_fine_init = 8e-5,
    densify_grad_threshold_after = 8e-5,
)
