# RaceColumn MPS calibration test: same as bouncingballs but with the
# densification gradient threshold lowered to match the Metal rasterizer's
# means2D gradient scale (gsplat pixel-units vs INRIA's NDC-calibrated 2e-4).
_base_ = './bouncingballs.py'
OptimizationParams = dict(
    densify_grad_threshold_coarse = 3e-8,
    densify_grad_threshold_fine_init = 3e-8,
    densify_grad_threshold_after = 3e-8,
)
