# RaceColumn MPS densification config.
#
# Densification threshold for the Metal rasterizer's means2D gradient scale.
# _native.py converts the means2D gradient to NDC (x W/2, H/2) to match INRIA's
# convention (depth-diff-gaussian-rasterization backward.cu:460,545:
# dL_dmean2D = dL/d(delta) * 0.5*W). Measured against a healthy state our
# accumulated stat is still ~5x below INRIA's at the p99 level, so the
# principled threshold is ~2e-4/5 ~= 4e-5 (vs the INRIA default 2e-4).
#
# CAVEAT: this cannot be properly validated yet. bouncingballs is a *dynamic*
# scene, and the deformation network is currently not learning the temporal
# motion on MPS (isolated: fine-stage training with fixed points leaves the
# mean test PSNR flat at ~14.6 over 4000 iters). An unfittable scene keeps the
# loss gradients high, so densification runs away regardless of threshold. The
# threshold below is the principled value; densification will only behave once
# the deformation-learning issue is fixed. See 4dgs-metal-rasterizer
# docs/M3_ROADMAP.md M4.
_base_ = './bouncingballs.py'
OptimizationParams = dict(
    densify_grad_threshold_coarse = 4e-5,
    densify_grad_threshold_fine_init = 4e-5,
    densify_grad_threshold_after = 4e-5,
)
