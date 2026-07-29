# RaceColumn MPS training config — stability recipe for training 4DGaussians
# on Apple MPS via the Metal rasterizer. Partial: fixes the total-failure and
# the fine-stage NaN divergence, but not yet the high-point-count instability
# (see 4dgs-metal-rasterizer docs/M3_ROADMAP.md M4).
#
# Findings that motivate each override:
#  - densify_grad_threshold: our means2D gradient is in INRIA's NDC convention
#    (_native.py x W/2; backward.cu:460) but measured ~5x below INRIA's stat at
#    p99, so ~2e-4/5 ~= 4e-5 (the INRIA default 2e-4 under-densifies here).
#  - opacity_lr 0.05 -> 0.01: at 0.05 opacity collapses to ~0.004 (all
#    transparent, matching the white background) before content can form,
#    starving the densification gradient. Lower keeps opacity rising.
#  - deformation_lr / grid_lr halved: these are multiplied by spatial_lr_scale
#    (~4.89 for this scene), which pushes the effective grid LR to ~8e-3 and
#    explodes the deformation into NaN once the fine stage engages.
#
# With these + gradient clipping in train.py, the early fine stage is stable
# and reconstructs (opacity recovers to ~0.05, densifies to ~48k), but it
# still destabilizes around 60-80k points. Remaining: high-point-count
# stability (densification schedule / opacity dynamics at scale).
_base_ = './bouncingballs.py'
OptimizationParams = dict(
    densify_grad_threshold_coarse = 4e-5,
    densify_grad_threshold_fine_init = 4e-5,
    densify_grad_threshold_after = 4e-5,
    opacity_lr = 0.01,
    deformation_lr_init = 0.00008,
    deformation_lr_final = 0.0000008,
    grid_lr_init = 0.0008,
    grid_lr_final = 0.000008,
)
